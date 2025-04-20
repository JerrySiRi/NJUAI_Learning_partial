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

    # -- 3. 定义一个把 ctx_list → CRF 特征 dict 序列的函数 -- #
    # 因为correct也要用，定义为类方法
    def make_crf_feats(self, ctx_list):
            if ctx_list == []:
                return None
            Xs = self.vectorizer.transform(ctx_list)
            feats = []
            for row in range(Xs.shape[0]):
                fv = {}
                row_coo = Xs[row].tocoo()
                for idx, val in zip(row_coo.col, row_coo.data):
                    fv[f"tfidf_{idx}"] = float(val)
                # 加一些离散特征
                ctx = ctx_list[row]
                fv['center'] = ctx[2]
                feats.append(fv)
            return feats

    def _train_ml_model(self, train_data: List[Dict[str, Any]]) -> None:
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
        
        # 法二：使用 TF‑IDF 特征训练 CRF 检测器和纠正器：
        # - 检测器：0/1 序列标注，判断是否出错
        # - 纠正器：多分类序列标注，预测正确字符
        
        from sklearn_crfsuite import CRF
        from sklearn_crfsuite.metrics import flat_classification_report
        import random
        
        # -- 1. 构造 detection 用的序列数据 -- #
        seq_feats, seq_det_labels = [], []
        
        # -- 2. 构造 correction 用的单点数据 -- #
        corr_contexts, corr_labels = [], []
        all_contexts = []

        add_all = 0
        add_previous = 0
        add_new = 0
        for sample in train_data:
            src, tgt = sample['source'], sample['target']
            if len(src) != len(tgt):
                continue

            # ---- 构造一条句子的 detection 特征/标签 ---- #
            feats_seq, det_seq = [], []
            for i in range(len(src)):
                # 丢掉边界太短的上下文
                if i-2 < 0 or i+3 > len(src):
                    continue
                ctx = src[i-2:i] + src[i] + src[i+1:i+3]
                all_contexts.append(ctx)
                feats_seq.append(ctx)
                det_seq.append('ERR' if src[i] != tgt[i] else 'OK')

                # ---- 如果这一位确实有错，再加到 correction 样本里 ---- #
                # BUG ？这一个假设是否合理？
                
                add_all += 1 
                if src[i] != tgt[i]: # 错误样本加入
                    corr_contexts.append(ctx)
                    corr_labels.append(tgt[i])
                    add_previous += 1
                    
                else: # 正确样本加入
                    prob = random.uniform(0,1)
                    if prob < 0.02:
                        corr_contexts.append(ctx)
                        corr_labels.append(tgt[i])
                        add_new += 1

            if feats_seq:
                seq_feats.append(feats_seq)
                seq_det_labels.append(det_seq)

        print(add_all, add_new, add_previous)
        
        # -- 2. TF‑IDF fit 所有上下文 -- #
        if not all_contexts:
            print("No contexts to fit TF-IDF, skip CRF.")
            return
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1,3), max_features=50)
        self.vectorizer.fit(all_contexts)
        
        X_det = [self.make_crf_feats(ctxs) for ctxs in seq_feats]
        y_det = seq_det_labels

        # -- 4. 训练检测 CRF -- #
        self.detector_model = CRF(
            algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=100,
            all_possible_transitions=True
        )
        self.detector_model.fit(X_det, y_det)
        print("[CRF-Detect] done")

        # -- 5. 准备纠正模型的训练数据 -- #
        # 把 corr_contexts, corr_labels 按“长度=1 的序列”包一层
        X_corr = [[self.make_crf_feats([ctx])[0]] for ctx in corr_contexts]
        y_corr = [[lbl] for lbl in corr_labels]

        if not X_corr:
            print("No error positions to train corrector CRF.")
            return

        # -- 6. 训练纠正 CRF -- #
        self.corrector_model = CRF(
            algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=30,
            all_possible_transitions=True
        )
        self.corrector_model.fit(X_corr, y_corr)
        print("[CRF-Correct] done")
        print(flat_classification_report(y_corr, self.corrector_model.predict(X_corr)))
        
        

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


    def _correct_with_ml(self, text: str) -> str:
        """
        Correct text using machine learning model.

        Args:
            text: Input text.

        Returns:
            Corrected text.
        """
        # TODO  
        # 先检测后纠正
        
        if not self.detector_model or not self.corrector_model:
            return text

        # -- 1) 构造所有位置的上下文（可能有 None）-- #
        ctxs = []
        for i in range(len(text)):
            if i-2 < 0 or i+3 > len(text):
                ctxs.append(None)
            else:
                ctx = text[i-2:i] + text[i] + text[i+1:i+3]
                # 只保留非空字符串
                ctxs.append(ctx if ctx else None)

        # -- 2) 过滤掉 None，得到真正要特征化的上下文列表 -- #
        valid_ctxs = [c for c in ctxs if c is not None]

        # 如果没有任何可用上下文，直接返回原文
        if not valid_ctxs:
            return text

        # -- 3) 用 TF-IDF+CRF 检测 -- #
        feat_seq = self.make_crf_feats(valid_ctxs)
        det_tags = self.detector_model.predict_single(feat_seq)

        # -- 4) 依次纠正被检测为 ERR 的位置 -- #
        corrected = list(text)
        vi = 0  # valid_ctxs 索引
        for idx, ctx in enumerate(ctxs):
            if ctx is None:
                continue  # 跳过没有上下文的位置
            if det_tags[vi] == 'ERR':
                # 构造单条特征并预测纠正字符
                single_feat = self.make_crf_feats([ctx])[0]
                corrected_char = self.corrector_model.predict_single([single_feat])[0]
                corrected[idx] = corrected_char
            vi += 1

        return ''.join(corrected)
