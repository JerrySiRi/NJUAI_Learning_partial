#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistical corrector for Chinese Text Correction task.
This module implements statistical methods for correcting errors in Chinese text.
"""

import re
import json
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
from transformers import BertTokenizer, BertModel
from typing import List, Dict
import Levenshtein


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
class DetCorrDataset(Dataset):
    def __init__(self, data: List[Dict[str, str]], tokenizer: BertTokenizer, max_len=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        src = self.data[idx]['source']
        tgt = self.data[idx]['target']
        # --- 1) encode src and tgt to ids --- #
        enc_src = self.tokenizer(src,
                                 padding='max_length',
                                 truncation=True,
                                 max_length=self.max_len,
                                 return_tensors='pt')
        enc_tgt = self.tokenizer(tgt,
                                 padding='max_length',
                                 truncation=True,
                                 max_length=self.max_len,
                                 return_tensors='pt')
        src_ids = enc_src.input_ids.squeeze(0)       # (L,)
        tgt_ids = enc_tgt.input_ids.squeeze(0)       # (L,)

        L = src_ids.size(0)
        pad_id = self.tokenizer.pad_token_id

        # --- 2) 初始化 labels --- #
        # 【det: 0=keep, 1=replace, 2=delete, 3=insert】
        det_labels = torch.zeros(L, dtype=torch.long)
        det_labels[src_ids == pad_id] = -100         # pad 忽略

        # corr: 正确的 token_id，只有 replace/insert 时才有意义
        corr_labels = torch.full((L,), -100, dtype=torch.long)

        # --- 3) 用 Levenshtein 对齐，生成操作 --- #
        # opcodes: List of (tag, i1,i2,j1,j2)
        ops = Levenshtein.opcodes(src, tgt)
        # 我们只对 src 长度内的位置打标，insert 会标在 i1 位置
        for tag, i1, i2, j1, j2 in ops:
            if tag == 'equal':
                continue
            elif tag == 'replace':
                # 每个被替换的 src[i] -> tgt[j]
                for si, tj in zip(range(i1, i2), range(j1, j2)):
                    if si < L:
                        det_labels[si] = 1
                        corr_labels[si] = self.tokenizer.convert_tokens_to_ids(tgt[tj])
            elif tag == 'delete':
                # 删除 src[i1:i2]
                for si in range(i1, i2):
                    if si < L:
                        det_labels[si] = 2
                        # corr_labels已经初始化了，继续保持 -100
            elif tag == 'insert':
                # 在 src[i1] 之前插入 tgt[j1:j2]，我们简化
                # 只保留第一个要插入的字符
                if i1 < L:
                    det_labels[i1] = 3
                    corr_labels[i1] = self.tokenizer.convert_tokens_to_ids(tgt[j1])
                # 若想插入多个字符，可扩展成列表，这里先做简化

        return {
            'input_ids':      src_ids,
            'attention_mask': enc_src.attention_mask.squeeze(0),
            'det_labels':     det_labels,
            'corr_labels':    corr_labels
        }

# Model: frozen BERT + BiLSTM + 两个头 -- detector & corrector
class BertBiLSTMDetCorr(nn.Module):
    def __init__(self, bert_model_name='bert-base-chinese', hidden_size=768, lstm_layers=1):
        super().__init__()
        
        self.bert = BertModel.from_pretrained(bert_model_name)
        
        # 【不冻结了！！！】
        # for p in self.bert.parameters():
        #     p.requires_grad = False
            
        self.bilstm = nn.LSTM(
            input_size=hidden_size, 
            hidden_size=hidden_size,
            num_layers=lstm_layers, 
            bidirectional=True, 
            batch_first=True
        )
        
        # ------ detector ------- #
        # 判断是不是错误的，output layer大小是2
        # self.det_fc = nn.Linear(hidden_size*2, 2)
        # 做四分类任务：正确的，替换，删除，插入
        self.det_fc = nn.Sequential(
            nn.Linear(hidden_size*2, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, hidden_size),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, 4)
        )
        
        
        # ------ corrector ------ # 
        # 纠正错误，必须要输出一个vocab_size的大小
        # 问题比较难，最后要映射到vocab_size的输出呢，估计需要更大的层级？
        self.corr_fc = nn.Sequential(
            nn.Linear(hidden_size*2, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, hidden_size*2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size*2, self.bert.config.vocab_size)
        )
        # 根据Bert的embedding先初始化一下
        # self.corr_fc[-1].weight = self.bert.embeddings.word_embeddings.weight
        
        # weight tying: 输出层权重 = BERT 的输入嵌入权重
        # self.corr_fc[-1].weight = self.bert.embeddings.word_embeddings.weight


    def forward(self, input_ids, attention_mask):
        # with torch.no_grad():
        enc = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        states = enc.last_hidden_state
        lstm_out, _ = self.bilstm(states)
        
        # 两个head单独接受LSTM的输出哦
        lstm_out, _ = self.bilstm(states)  # (B, L, 2H)
        det_logits  = self.det_fc(lstm_out)   # (B, L, 2)
        corr_logits = self.corr_fc(lstm_out)  # (B, L, V)
        return det_logits, corr_logits, lstm_out



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

    
    def _train_ml_model(self, model: BertBiLSTMDetCorr, \
                        train_data: List[Dict[str, str]], \
                        epochs=10, batch_size=16, max_len=128, lr=2e-5) -> None:
        
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
        
        train_split, val_split = train_test_split(
            train_data, test_size=0.05, random_state=42
        )
        
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        train_dataset = DetCorrDataset(train_split, tokenizer, max_len)
        val_dataset   = DetCorrDataset(val_split,   tokenizer, max_len)
        train_loader  = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader    = DataLoader(val_dataset,   batch_size=batch_size, shuffle=False)
        
        """
        optimizer = torch.optim.Adam(
            filter(lambda p: p.requires_grad, model.parameters()), lr=lr
        )
        """
        
        bert_params, decoder_params = [], []
        for name, p in model.named_parameters():
            if 'bert' in name:
                bert_params.append(p)
            else:
                decoder_params.append(p)
        optimizer = torch.optim.Adam([
            {'params': bert_params,     'lr': 2e-5},   # BERT 用小 lr
            {'params': decoder_params,  'lr': 1e-3},   # decoder (BiLSTM) 用大 lr
        ])

        
        """
        # 【类别不平衡 - label = 0（正确的）过多】
        from collections import Counter
        counts = Counter()
        for batch in train_loader:
            labs = batch['det_labels'].view(-1).cpu().tolist()
            counts.update([l for l in labs if l >= 0])  # 忽略 -100
        print("Unbalanced data", counts)     
        """
        
        # ------ Unbalanced data Counter({0: 101392, 1: 696, 2: 261, 3: 183}) ------ #
        
        all_labels = torch.cat([b['det_labels'].view(-1) for b in train_loader])
        all_labels = all_labels[all_labels >= 0]
        N = float(len(all_labels))
        weights = []
        for cls in range(4):
            cnt = int((all_labels == cls).sum().item())
            # 避免除零
            weights.append(N/cnt if cnt>0 else 0.0)
        weight_tensor = torch.tensor(weights, device=self.device)
        
        det_criterion = nn.CrossEntropyLoss(weight=weight_tensor, ignore_index=-100)
        corr_criterion = nn.CrossEntropyLoss(ignore_index=-100)
        

        model.to(self.device) 
        model.train()
        for epoch in range(epochs):
            # —— 训练阶段 —— #
            loop = tqdm(train_loader, desc=f"Train Epoch {epoch+1}/{epochs}")
            total_det_loss = total_corr_loss = 0.0
            for batch in loop:
                input_ids     = batch['input_ids'].to(self.device)
                attention_mask= batch['attention_mask'].to(self.device)
                det_labels    = batch['det_labels'].to(self.device)
                corr_labels   = batch['corr_labels'].to(self.device)

                det_logits, corr_logits, _ = model(input_ids, attention_mask)
                
                # BUG：改成 4分类任务，下面都得改啦
                # 原 det_logits 的 shape 是 (B, L, 4)
                B, L, num_det_classes = det_logits.size()  # num_det_classes 应当是 4

                # 训练损失时，把它 flatten 成 (B*L, 4)
                det_loss = det_criterion(
                    det_logits.view(-1, num_det_classes),  # (B*L, 4)
                    det_labels.view(-1)                    # (B*L,)
                )

                # corr_logits 依然是 (B, L, V)
                V = corr_logits.size(-1)
                corr_loss = corr_criterion(
                    corr_logits.view(-1, V),              # (B*L, V)
                    corr_labels.view(-1)                  # (B*L,)
                )

                loss = det_loss + corr_loss

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_det_loss  += det_loss.item()
                total_corr_loss += corr_loss.item()
                loop.set_postfix({
                    'd_l': total_det_loss/(loop.n+1),
                    'c_l': total_corr_loss/(loop.n+1),
                    't_l': (total_det_loss + total_corr_loss)/(loop.n+1)
                })

            avg_train_det  = total_det_loss  / len(train_loader)
            avg_train_corr = total_corr_loss / len(train_loader)

            # -- 验证阶段 -- #
            model.eval()
            val_det_loss = val_corr_loss = 0.0
            with torch.no_grad():
                for batch in val_loader:
                    input_ids      = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    det_labels     = batch['det_labels'].to(self.device)
                    corr_labels    = batch['corr_labels'].to(self.device)

                    det_logits, corr_logits, _ = model(input_ids, attention_mask)
                
                    # BUG：改成 4分类任务，下面都得改啦
                    # 原 det_logits 的 shape 是 (B, L, 4)
                    B, L, num_det_classes = det_logits.size()  # num_det_classes 应当是 4

                    # 训练损失时，把它 flatten 成 (B*L, 4)
                    det_loss = det_criterion(
                        det_logits.view(-1, num_det_classes),  # (B*L, 4)
                        det_labels.view(-1)                    # (B*L,)
                    )

                    # corr_logits 依然是 (B, L, V)
                    V = corr_logits.size(-1)
                    corr_loss = corr_criterion(
                        corr_logits.view(-1, V),              # (B*L, V)
                        corr_labels.view(-1)                  # (B*L,)
                    )

                    val_det_loss  += det_loss.item()
                    val_corr_loss += corr_loss.item()

            avg_val_det  = val_det_loss  / len(val_loader)
            avg_val_corr = val_corr_loss / len(val_loader)
            model.train()

            print(
                f"Epoch {epoch+1} >>>>>>>>>>> "
                f"Train Loss(det, corr): {avg_train_det:.4f}, {avg_train_corr:.4f} | "
                f"Val Loss(det, corr): {avg_val_det:.4f}, {avg_val_corr:.4f}"
            )
        

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


    def _correct_with_ml(self, model: BertBiLSTMDetCorr, text: str, max_len=128) -> str:
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
        
        tok = BertTokenizer.from_pretrained('bert-base-chinese')
        enc = tok(text,
                return_tensors='pt',
                max_length=max_len,
                truncation=True,
                padding='max_length',
                add_special_tokens=True)
        input_ids = enc.input_ids.to(self.device)
        attn_mask = enc.attention_mask.to(self.device)

        with torch.no_grad():
            det_logits, corr_logits, lstm_out = model(input_ids, attn_mask)
        # 把 pad 位置 (mask==0) 的 logits 设为一个很小的值
        mask = attn_mask.unsqueeze(-1).expand_as(det_logits)  # (1, L, 4)
        det_logits = det_logits.masked_fill(~mask.bool(), -1e9)
        # "~"对布尔张量做按位取反，得到：True 表示要屏蔽的位置，False 表示保留
        det_preds  = det_logits.argmax(dim=-1).squeeze(0)  # pad 处必然是 0 (keep)
        corr_preds = corr_logits.argmax(-1).squeeze(0) # (L,)

        # print("Detector prediction",det_preds)
        # 原文字列表
        chars = list(text)
        out = []
        i = 0
        
        flag = False
        if len(chars) > self.max_length:
            flag = True
        
        # 部分超过上下文长度啦
        while i < min(len(chars), self.max_length-1):
            tok_idx = i + 1  # 对应 BERT token 下标，一开始有一个[CLS]呢~
            op = det_preds[tok_idx].item()

            if op == 0:
                # keep
                out.append(chars[i])
                i += 1
            elif op == 1:
                # replace
                new_id = corr_preds[tok_idx].item()
                new_tok = tok.convert_ids_to_tokens([new_id])[0]
                out.append(new_tok)
                i += 1
            elif op == 2:
                # delete: 跳过原字符
                i += 1
            elif op == 3:
                # insert: 在当前位置插入 corr_preds，然后不跳过原字符
                new_id = corr_preds[tok_idx].item()
                new_tok = tok.convert_ids_to_tokens([new_id])[0]
                out.append(new_tok)
                # 原字符也保留
                out.append(chars[i])
                i += 1
            else:
                # padding / unknown
                out.append(chars[i])
                i += 1

        # 处理超过self.max_length的例子的后续，使得就算没法纠正，也可以正常输出
        if flag == True:
            result = ''.join(out) + ''.join(chars[self.max_length-1: ])
        else:
            result = ''.join(out)
        # print(result)
        return result