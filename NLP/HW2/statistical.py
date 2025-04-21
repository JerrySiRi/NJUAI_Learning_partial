#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistical corrector for Chinese Text Correction task.
This module implements statistical methods for correcting errors in Chinese text.
"""

import re
import json
import copy
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter, defaultdict

# Try to import optional dependencies
try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("Warning: jieba not available. Some features will be disabled.")

try:
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score

    # Import CRF if available
    try:
        import sklearn_crfsuite
        from sklearn_crfsuite import metrics

        CRF_AVAILABLE = True
    except ImportError:
        CRF_AVAILABLE = False
        print("Warning: sklearn_crfsuite not available. CRF features will be disabled.")

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    CRF_AVAILABLE = False
    print("Warning: scikit-learn not available. Some features will be disabled.")


# --------- 新引入的 --------- #
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup
from typing import List, Dict
import Levenshtein
from torchcrf import CRF


"""
改进措施：
 -- 模型结构设计与优化 -- 
1.不冻结Bert的参数了。 BERT虽提供通用语言特征，但未经微调就直接用于细粒度的错误检测，效果可能不佳
 https://aclanthology.org/2020.acl-main.82.pdf
 【结论：有用，但是用处不大，从0.001 -> 0.003】

2. Bert + CRF直接预测
    理论上BERT自身已经是深层双向Transformer，具备丰富的上下文信息。
   额外的BiLSTM可能贡献有限，却增加了参数和过拟合风险。
   可以考虑替换或简化BiLSTM层：
   一方面可以尝试直接使用BERT最后一层输出接分类头（类似于序列标注的BERT+CRF常见架构），减少模型复杂度；
   另一方面，如果希望利用序列标注的标签依赖，可引入CRF层替代BiLSTM，用于学习标签的全局约束（如避免无效的标签序列）。
   CRF能够确保输出操作序列的一致性，但也会增加计算量。
   【基于目前数据规模，优先考虑去除或简化BiLSTM，让BERT的表示直接服务于分类，以减少过拟合】

3. 不能只用linear层是独立的了，detector和corrector共享bert的输出

-- 训练任务修改 --  

1. detection：只做二分类 - 正确 & 错误【减少四选一 & 类别不平衡
   correction：决定具体是哪种操作以及相应的纠正内容。
            即在检测为错误的位置上执行细粒度分类（替换/删除/插入）并输出纠正的字符。
    

"""


# 准备数据格式：detection + correction
class SeqOpDataset(Dataset):
    """
    Dataset for joint 4-way sequence labeling + character generation.
    Labels:
      op_labels: 0=KEEP,1=REPLACE,2=DELETE,3=INSERT
      corr_labels: token_id for REPLACE/INSERT, -100 otherwise
    """
    def __init__(self, data: List[Dict[str,str]], tokenizer, max_len=128):
        self.data = data
        self.tk   = tokenizer
        self.max_len = max_len

    def __len__(self): return len(self.data)

    def __getitem__(self, i):
        src = self.data[i]['source']
        tgt = self.data[i]['target']
        enc = self.tk(src, padding='max_length', truncation=True,
                      max_length=self.max_len, return_tensors='pt',
                      add_special_tokens=True)
        ids = enc.input_ids.squeeze(0)
        mask= enc.attention_mask.squeeze(0)
        L   = ids.size(0)
        pad = self.tk.pad_token_id

        # 初始化 op_labels 和 corr_labels
        op_labels   = torch.zeros(L, dtype=torch.long)
        op_labels[ids==pad] = -100
        corr_labels = torch.full((L,), -100, dtype=torch.long)

        # Levenshtein 对齐
        ops = Levenshtein.opcodes(src, tgt)
        for tag,i1,i2,j1,j2 in ops:
            for si,tj in zip(range(i1,i2), range(j1,j2)):
                tok_idx = si+1  # 跳过 [CLS]
                if tok_idx>=L-1: break
                if tag=='replace':
                    op_labels[tok_idx]=1
                    corr_labels[tok_idx] = self.tk.convert_tokens_to_ids(tgt[tj])
                elif tag=='delete':
                    op_labels[tok_idx]=2
                elif tag=='insert':
                    op_labels[tok_idx]=3
                    corr_labels[tok_idx] = self.tk.convert_tokens_to_ids(tgt[j1])
                # equal -> keep (0)

        return {
            'input_ids': ids,
            'attention_mask': mask,
            'op_labels': op_labels,
            'corr_labels': corr_labels
        }

class CharCorrectionHead(nn.Module):
    """
    字符纠正头：MLP → BiLSTM → Linear(vocab)
    输入 (B, L, H)，输出 (B, L, V)
    """
    def __init__(self, hidden_size: int, vocab_size: int,
                 dropout: float = 0.1, lstm_layers: int = 1):
        super().__init__()
        
        # -- 两层 MLP -- #
        self.mlp = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.GELU(),
            nn.Dropout(dropout),

            nn.Linear(hidden_size, hidden_size),
            nn.GELU(),
            nn.Dropout(dropout),
        )
        # -- BiLSTM -- #
        self.bilstm = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size // 2,
            num_layers=lstm_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if lstm_layers > 1 else 0.0
        )
        
        # -- 最终投到 vocab_size -- #
        self.out = nn.Linear(hidden_size, vocab_size)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
          x: (B, L, H)
        Returns:
          (B, L, V)
        """
        x = self.mlp(x)              # (B, L, H)
        x, _ = self.bilstm(x)        # (B, L, H)
        return self.out(x)           # (B, L, V)
        

class BertCRFCorrector(nn.Module):
    def __init__(self,
                 model_name: str = 'bert-base-chinese',
                 hidden: int = 768,
                 dropout: float = 0.1,
                 lstm_layers: int = 1):
        
        super().__init__()
        # -- BERT 编码器 -- # 
        self.bert = BertModel.from_pretrained(model_name)
        self.drop = nn.Dropout(dropout)

        # -- 4-way 操作 CRF -- #
        self.op_fc  = nn.Linear(hidden, 4)
        self.op_crf = CRF(num_tags=4, batch_first=True)

        # -- 字符预测头 -- #
        # -- 字符纠正分支 —— 全部放到 self.char_fc -- #
        self.char_fc = CharCorrectionHead(
            hidden_size=hidden,
            vocab_size=self.bert.config.vocab_size,
            dropout=dropout,
            lstm_layers=lstm_layers
        )
        
        # nn.Linear(hidden, self.bert.config.vocab_size)

    def forward(self,
                ids: torch.LongTensor,
                mask: torch.LongTensor,
                op_labels: torch.LongTensor = None,
                corr_labels: torch.LongTensor = None):
        """
        Args:
          ids         (B, L)   BERT 输入 id
          mask        (B, L)   attention_mask （0/1 LongTensor）
          op_labels   (B, L)   0=KEEP,1=REPLACE,2=DELETE,3=INSERT, -100=ignore
          corr_labels (B, L)   纠正字符 id（只有 replace/insert 有效），-100=ignore

        Returns:
          loss_op    – None or scalar 操作 CRF 的负对数似然
          loss_char  – None or scalar 字符预测的交叉熵
          op_logits  – (B, L, 4) CRF 前的原始得分
          char_logits– (B, L, V) 字符预测 logits
        """
        
        # --- BERT 编码 ---
        bert_out = self.bert(input_ids=ids, attention_mask=mask)
        seq_out  = bert_out.last_hidden_state   # (B, L, H)
        seq_out  = self.drop(seq_out)

        # BUG 强制把 mask 转成 BoolTensor
        bool_mask = mask.bool()                 # (B, L)

        # --- 操作 CRF 前向 ---
        op_logits = self.op_fc(seq_out)         # (B, L, 4)
        loss_op = None
        if op_labels is not None:
            # 复制并修正越界标签
            tags = op_labels.clone()
            tags[tags < 0]  = 0
            tags[tags >= 4] = 0
            
            ll = self.op_crf(op_logits, tags, mask=bool_mask)
            loss_op = -ll.mean()

        # --- 字符预测头 & 损失 ---
        char_logits = self.char_fc(seq_out)     # (B, L, V)
        loss_char = None
        if corr_labels is not None:
            B, L, V = char_logits.size()
            flat_logits = char_logits.view(-1, V)    # (B*L, V)
            flat_labels = corr_labels.view(-1)       # (B*L,)
            ce = nn.CrossEntropyLoss(ignore_index=-100)
            loss_char = ce(flat_logits, flat_labels)

        return loss_op, loss_char, op_logits, char_logits


class StatisticalCorrector:
    """
    A statistical corrector for Chinese text.
    """

    def __init__(self, method='ngram'):
        """
        Initialize the statistical corrector.

        Args:
            method: The statistical method to use. Options: 'ngram', 'ml', 'crf'.
        """
        self.method = method

        # N-gram language model
        self.unigram_counts = Counter()
        self.bigram_counts = Counter()
        self.trigram_counts = Counter()
        self.fourgram_counts = Counter()  # 4-gram for better context modeling

        # Character-level confusion matrix
        self.confusion_matrix = defaultdict(Counter)

        # Character error probabilities
        self.error_probs = defaultdict(float)

        # Phonetic and visual similarity matrices
        self.phonetic_similarity = defaultdict(dict)
        self.visual_similarity = defaultdict(dict)

        # Interpolation weights for different n-gram models
        self.lambda_1 = 0.1  # Weight for unigram
        self.lambda_2 = 0.3  # Weight for bigram
        self.lambda_3 = 0.4  # Weight for trigram
        self.lambda_4 = 0.2  # Weight for 4-gram

        # Machine learning models
        self.ml_model = None
        self.vectorizer = None
        self.feature_scaler = None
        # 使用crf
        self.detector_model = None
        self.corrector_model = None

        # Character corrections dictionary
        self.char_corrections = defaultdict(Counter)
        
        # Bert模型确定device时
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    def train(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Train the statistical corrector using the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        if self.method == 'ngram':
            self._train_ngram_model(train_data)
        elif self.method == 'ml' and SKLEARN_AVAILABLE:
            self._train_ml_model(train_data)
        else:
            print(f"Warning: Method '{self.method}' not available. Falling back to n-gram model.")
            self._train_ngram_model(train_data)


    def _train_ngram_model(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Train an n-gram language model for text correction.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO 完成ngram模型，可以使用其他的设计
        # Build n-gram language model from correct sentences
        for sample in train_data:
            # Use target (correct) text for building the language model
            text = sample['target']

            # TODO Count bigrams, trigrams, and 4-grams
            # Count unigrams (single characters)
            for char in text:
                self.unigram_counts[char] += 1
             # Bigram
            for i in range(len(text) - 1):
                self.bigram_counts[text[i : i + 2]] += 1
            # Trigram
            for i in range(len(text) - 2):
                self.trigram_counts[text[i : i + 3]] += 1
            # Four-gram
            for i in range(len(text) - 3):
                self.fourgram_counts[text[i : i + 4]] += 1
            
            # Build confusion matrix from error pairs
            if sample['label'] == 1:  # Only for sentences with errors
                source = sample['source']
                target = sample['target']

                # For character substitution errors (when lengths are equal)
                if len(source) == len(target):
                    for i, (s_char, t_char) in enumerate(zip(source, target)):
                        if s_char != t_char:
                            
                            # Record this confusion pair with context
                            left_context = source[max(0, i - 2) : i]
                            right_context = source[i + 1 : min(len(source), i + 3)]
                            context = left_context + '_' + right_context

                            self.confusion_matrix[(s_char, context)][t_char] += 1

                            # Also record general confusion without context
                            self.confusion_matrix[(s_char, '')][t_char] += 1

                            # Record error probability for this character
                            self.error_probs[s_char] += 1

                            # Record correction pair
                            self.char_corrections[s_char][t_char] += 1

        # Normalize error probabilities
        for char, count in self.error_probs.items():
            self.error_probs[char] = count / self.unigram_counts.get(char, 1)

        print(
                f"Trained n-gram model with {len(self.unigram_counts)} unigrams, "
                f"{len(self.bigram_counts)} bigrams, "
                f"{len(self.trigram_counts)} trigrams, "
                f"{len(self.fourgram_counts)} 4-grams."
            )

    
    def _train_ml_model(self, model: BertCRFCorrector, \
                        train_data: List[Dict[str, str]], \
                        epochs=8, batch_size=8, max_len=128, lr=2e-5) -> None:
        
        self.max_length = max_len
        """
        Train a machine learning model for text correction.

        Args:
            train_data: List of dictionaries containing the training data.
        """

        if not SKLEARN_AVAILABLE:
            print("Cannot train ML model: scikit-learn not available.")
            return
                
        # TODO 完成ml方法实现，可选择不同的文本编码方式、不同的特征提取和不同的模型,
        # 推荐先使用一个模型检测，再使用一个模型来纠错。
        # 可以先将训练数据分为训练集和验证集，分别检测两个模型的效果，并调参
        # 可以使用数据增强或者预训练的词向量来提高模型的准确性
        
        from tqdm.auto import tqdm
        from torch.utils.data import DataLoader, WeightedRandomSampler
        
        tk     = BertTokenizer.from_pretrained('bert-base-chinese')

        train_d, val_d = train_test_split(train_data, test_size=0.1, random_state=42)

        # 采样权重
        sample_weights = []
        for sample in train_d:
            src, tgt = sample['source'], sample['target']
            ops = Levenshtein.opcodes(src, tgt)
            # errs = replace + delete + insert 次数
            errs = sum(1 for tag, *_ in ops if tag != 'equal')
            sample_weights.append(errs + 1)  # errs=0 的句子也保留权重 1

        sampler = WeightedRandomSampler(
            weights=sample_weights,
            num_samples=len(sample_weights),
            replacement=True
        )

        # Dataset & DataLoader
        train_ds = SeqOpDataset(train_d, tk, max_len)
        val_ds   = SeqOpDataset(val_d,   tk, max_len)

        train_loader = DataLoader(
            train_ds,
            batch_size=batch_size,
            sampler=sampler,   # 用 sampler 代替 shuffle !!!!
            drop_last=False,
            pin_memory=True,
            num_workers=2
        )
        val_loader   = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

        # 其他和以前相同：优化器、scheduler
        optimizer = AdamW(model.parameters(), lr=lr, weight_decay=0.01)
        total_steps = epochs * len(train_loader)
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=int(0.1 * total_steps),
            num_training_steps=total_steps
        )

        model.to(self.device)
        for ep in range(epochs):
            model.train()
            tot_op = tot_ch = 0.0
            for batch in tqdm(train_loader, desc=f"Train Epoch {ep+1}/{epochs}"):
                
                # 所有的数据都移到 device
                for k,v in batch.items():
                    batch[k] = v.to(self.device)
                optimizer.zero_grad()
                loss_op, loss_char, op_logits, char_logits = model(
                    batch['input_ids'],
                    batch['attention_mask'],
                    batch['op_labels'],
                    batch['corr_labels']
                )
                
                
                loss = loss_op + 1.5*loss_char
                loss.backward()
                optimizer.step()
                scheduler.step()
                tot_op += loss_op.item()
                tot_ch += loss_char.item()
                # print("\n Loss Operation", tot_op)
                # print("\n Loss Character", tot_ch)
            print(f"Ep{ep+1} op_loss={tot_op/len(train_loader):.4f}  char_loss={tot_ch/len(train_loader):.4f}")

            # 验证
            model.eval()
            vop = vch = 0.0
            with torch.no_grad():
                for batch in val_loader:
                    for k,v in batch.items():
                        batch[k] = v.to(self.device)
                    loss_op, *_ = model(
                        batch['input_ids'],
                        batch['attention_mask'],
                        batch['op_labels'],
                        batch['corr_labels']
                    )
                    vop += loss_op.item()
            print(f" Val op_loss={vop/len(val_loader):.4f}")
        

    def correct(self, text: str) -> str:
        """
        Apply statistical correction to the input text.

        Args:
            text: Input text to correct.

        Returns:
            Corrected text.
        """
        if self.method == 'ngram':
            return self._correct_with_ngram(text)
        elif self.method == 'ml' and SKLEARN_AVAILABLE and \
                        (self.corrector_model is not None) and (self.detector_model is not None):
            return self._correct_with_ml(text)
        
        else:
            return self._correct_with_ngram(text)


    def _correct_with_ngram(self, text: str) -> str:
        """
        Correct text using the n-gram language model.

        Args:
            text: Input text.

        Returns:
            Corrected text.
        """
        corrected_text = list(text)  # Convert to list for character-by-character editing
        # Check each character for potential errors
        for i in range(len(text)):
            char = text[i]

            # Skip characters with low error probability
            if self.error_probs.get(char, 0) < 0.01:
                continue

            # Get context for this character
            left1 = text[max(0, i - 1) : i]
            left2 = text[max(0, i - 2) : i]
            left3 = text[max(0, i - 3) : i]
            right1 = text[i + 1 : min(len(text), i + 2)]
            right2 = text[i + 1 : min(len(text), i + 3)]
            right3 = text[i + 1 : min(len(text), i + 4)]
            
            context = left2 + '_' + right2

            # 1. 精确上下文纠错
            # Check if we have seen this character in this context before
            if (char, context) in self.confusion_matrix and self.confusion_matrix[(char, context)]:
                # Get the most common correction for this character in this context
                correction = self.confusion_matrix[(char, context)].most_common(1)[0][0]
                corrected_text[i] = correction
                continue
            
            # 2. 通用混淆矩阵
            # If no specific context match, check general confusion matrix
            if (char, '') in self.confusion_matrix and self.confusion_matrix[(char, '')]:
                # Get the most common correction for this character
                correction = self.confusion_matrix[(char, '')].most_common(1)[0][0]
                # Only apply if it's a common error
                if self.confusion_matrix[(char, '')][correction] > 2:
                    corrected_text[i] = correction
                    continue
            
            # 3. n-gram 评分
            # If no direct match, use interpolated n-gram model for characters with high error probability
            if self.error_probs.get(char, 0) >= 0.05 and i > 0 and i < len(text) - 1:
                
                # Generate candidate corrections
                candidates = set()
                # Add common characters as candidates
                candidates.update(list(self.unigram_counts.keys())[:300])  # Top 300 most common characters
                # Add correction candidates from confusion matrix
                for context_key in self.confusion_matrix:
                    if context_key[0] == char:
                        candidates.update(self.confusion_matrix[context_key].keys())
                        
                # ------- n-gram的 插值评分函数 -------- # 
                # TODO Bigram, trigram, and 4-gram probabilities
                V = len(self.unigram_counts)
                total_unigrams = sum(self.unigram_counts.values())
                
                def score(cand: str) -> float:
                    sc = 0.0
                    # Unigram
                    uni_p = (self.unigram_counts.get(cand, 0) + 1) / (total_unigrams + V)
                    sc += self.lambda_1 * uni_p
                    # Bigram 左上下文
                    if left1:
                        bi = left1[-1] + cand
                        bi_p = (self.bigram_counts.get(bi, 0) + 1) / (self.unigram_counts.get(left1[-1], 0) + V)
                        sc += self.lambda_2 * bi_p
                    # Trigram 左上下文
                    if len(left2) == 2:
                        tri = left2 + cand
                        tri_p = (self.trigram_counts.get(tri, 0) + 1) / (self.bigram_counts.get(left2, 0) + V)
                        sc += self.lambda_3 * tri_p
                    # Four-gram (left2 + cand + right1)
                    if len(left2) == 2 and right1:
                        four = left2 + cand + right1
                        four_p = (self.fourgram_counts.get(four, 0) + 1) / (self.trigram_counts.get(left2 + cand, 0) + V)
                        sc += self.lambda_4 * four_p
                    return sc


                # -------- 逐个candidate计算n-gram评分 -------- #
                # Try all candidates and find the one with highest probability
                best_score = -float('inf')
                best_char = char

                original_score = score(char)
                best_char, best_score = char, -1e9
                for cand in candidates:
                    if cand == char:
                        continue
                    sc = score(cand)
                    if sc > best_score:
                        best_score, best_char = sc, cand

                # Only replace if the new score is significantly better
                threshold = 1.2 + self.error_probs.get(char, 0) * 3  # Dynamic threshold based on error probability
                if best_score > original_score * threshold:
                    corrected_text[i] = best_char

        return ''.join(corrected_text)


    def _correct_with_ml(self, model: BertCRFCorrector, text: str, max_len=128) -> str:
        """
        Correct text using machine learning model.

        Args:
            text: Input text.

        Returns:
            Corrected text.
        """
        # TODO  
        # 先检测后纠正

        import re
        model.to(self.device)
        model.eval()
        
        # 中文字符正则
        _chinese_char = re.compile(r'[\u4e00-\u9fff]')
        # 其他位置（标点、英文、数字、空格）均跳过。
        # 这样就不会再把逗号，、句号。等都替换成“的”了
        
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        enc = tokenizer(text,
                        return_tensors='pt',
                        max_length=max_len,
                        truncation=True,
                        padding='max_length',
                        add_special_tokens=True)
        ids  = enc.input_ids.to(self.device)
        mask = enc.attention_mask.to(self.device)

        model.to(self.device).eval()
        with torch.no_grad():
            loss_op, loss_ch, op_logits, char_logits = model(ids, mask)

        # decode 4-way operations
        tags = model.op_crf.decode(op_logits, mask.bool())[0]  # list of length L
        chars = list(text)
        out = []
        
            
        flag = False
        index_trun = 0
        
        for i, ch in enumerate(chars):
            tok_idx = i + 1
            if tok_idx > len(tags) - 1:
                flag = True
                index_trun = i
                continue
            # print(tok_idx)
            op = tags[tok_idx]
            if op == 0:            # KEEP
                out.append(ch)
            elif op == 1:          # REPLACE
                logits = char_logits[0, tok_idx]
                cid = logits.argmax().item()
                new = tokenizer.convert_ids_to_tokens([cid])[0]
                out.append(new)
            elif op == 2:          # DELETE
                continue
            elif op == 3:          # INSERT
                logits = char_logits[0, tok_idx]
                cid = logits.argmax().item()
                new = tokenizer.convert_ids_to_tokens([cid])[0]
                out.append(new)
                out.append(ch)
         # 处理超过self.max_length的例子的后续，使得就算没法纠正，也可以正常输出
        if flag == True:
            result = ''.join(out) + ''.join(chars[index_trun: ])
        else:
            result = ''.join(out)
        # print(result)
        return result
