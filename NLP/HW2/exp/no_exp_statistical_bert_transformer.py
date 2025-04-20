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


# Dataset for sequence tagging
class SeqCorrDataset(Dataset):
    def __init__(self, data: List[Dict[str, str]], tokenizer: BertTokenizer, max_len=128):
        self.pairs = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        src = self.pairs[idx]['source']
        tgt = self.pairs[idx]['target']
        enc = self.tokenizer(src, padding='max_length', truncation=True,
                             max_length=self.max_len, return_tensors='pt')
        tgt_enc = self.tokenizer(tgt, padding='max_length', truncation=True,
                                 max_length=self.max_len, return_tensors='pt')
        return {
            'input_ids': enc.input_ids.squeeze(0),
            'attention_mask': enc.attention_mask.squeeze(0),
            'labels': tgt_enc.input_ids.squeeze(0)
        }

# Transformer-based decoder with frozen BERT encoder
class BertTransformerCorrector(nn.Module):
    def __init__(self,
                 bert_model_name='bert-base-chinese',
                 d_model=768,
                 nhead=8,
                 num_layers=3,
                 dim_feedforward=2048,
                 dropout=0.1,
                 max_len=128):
        super().__init__()
        self.max_len = max_len
        
        # load and freeze BERT
        self.bert = BertModel.from_pretrained(bert_model_name)
        
        # 把BERT的模型参数给固定住
        for bert_para in self.bert.parameters():
            bert_para.requires_grad = False
        
        # bert自己基于word-level的embedding
        self.embedding = self.bert.embeddings

        # positional encoding
        self.pos_encoder = nn.Embedding(self.max_len, d_model)

        # Transformer decoder
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout
        )
        self.transformer_decoder = nn.TransformerDecoder(
            decoder_layer,
            num_layers=num_layers
        )
        # output projection
        self.output_proj = nn.Linear(d_model, self.bert.config.vocab_size)

    def forward(self,
                input_ids: torch.Tensor,
                attention_mask: torch.Tensor,
                decoder_input_ids: torch.Tensor):
        """
        input_ids: (B, L)
        attention_mask: (B, L)
        decoder_input_ids: (B, L)  -- teacher forcing inputs
        """
        
        # BERT encoder
        with torch.no_grad():
            enc_outputs = self.bert(input_ids=input_ids,
                                     attention_mask=attention_mask)
        memory = enc_outputs.last_hidden_state.transpose(0,1)  # (L, B, D)

        # decoder embeddings + positional encoding
        tgt_emb = self.embedding(decoder_input_ids)  # (B, L, D)
        positions = torch.arange(decoder_input_ids.size(1), device=decoder_input_ids.device)
        pos_emb = self.pos_encoder(positions).unsqueeze(0)  # (1, L, D)
        tgt = (tgt_emb + pos_emb).transpose(0,1)            # (L, B, D)

        # causal mask for decoder
        seq_len = decoder_input_ids.size(1)
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(seq_len).to(tgt.device)

        # decode
        output = self.transformer_decoder(
            tgt,
            memory,
            tgt_mask=tgt_mask,
            memory_key_padding_mask=~attention_mask.bool()
        )  # (L, B, D)
        output = output.transpose(0,1)  # (B, L, D)
        logits = self.output_proj(output)  # (B, L, V)
        return logits


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

    
    def _train_ml_model(self, model: BertTransformerCorrector, \
                       train_data: List[Dict[str,str]],
                           epochs=3, batch_size=16, lr=1e-4,
                           max_len=128, device=None) -> None:
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
            
        model.to(device)

        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        dataset = SeqCorrDataset(train_data, tokenizer, max_len=max_len)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)
        criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)

        model.train()
        for epoch in range(epochs):
            loop = tqdm(loader, desc=f"Epoch {epoch+1}/{epochs}")
            total_loss = 0.0
            for batch in loop:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                # prepare decoder inputs
                decoder_input_ids = torch.cat([
                    torch.full((labels.size(0),1), tokenizer.cls_token_id,
                            dtype=torch.long, device=device),
                    labels[:,:-1]
                ], dim=1)
                logits = model(input_ids, attention_mask, decoder_input_ids)
                loss = criterion(logits.view(-1, logits.size(-1)),
                                labels.view(-1))
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                loop.set_postfix(loss=total_loss/(loop.n+1))
            print(f"Epoch {epoch+1} avg loss: {total_loss/len(loader):.4f}")
        

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


    def _correct_with_ml(self, model: BertTransformerCorrector, text: str, max_len=128) -> str:
        """
        Correct text using machine learning model.

        Args:
            text: Input text.

        Returns:
            Corrected text.
        """
        # TODO  
        # 先检测后纠正
        model.to(self.device).eval()

        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        enc = tokenizer(text, return_tensors='pt',
                        max_length=max_len, truncation=True,
                        padding='max_length')
        input_ids = enc.input_ids.to(self.device)
        attention_mask = enc.attention_mask.to(self.device)

        # iterative decode
        generated = [tokenizer.cls_token_id]
        with torch.no_grad():
            for _ in range(max_len-1):
                decoder_input_ids = torch.tensor([generated + [tokenizer.pad_token_id]*(max_len-1-len(generated))],
                                                device=self.device)
                logits = model(input_ids, attention_mask, decoder_input_ids)
                next_token = logits[0, len(generated)-1].argmax().item()
                if next_token == tokenizer.sep_token_id:
                    break
                generated.append(next_token)
        decoded = tokenizer.decode(generated, skip_special_tokens=True)
        return decoded
