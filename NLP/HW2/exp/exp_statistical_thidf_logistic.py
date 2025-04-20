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
        
        
        # ---- 法一：构造字符级上下文特征（char-3gram TF-IDF + 逻辑回归） ---- #
        # 理解：把纠错任务看成多分类问题
        # x：(左2，中心，右2)
        # y：target中心词
        
        # -- 1. 构造样本 -- #
        contexts_all, detect_labels = [], [] # detection model根据 上下文 -> label=1/-1，判断是否是错误的
        contexts_err, correct_labels = [], [] # correction model根据 上下文 -> 正确的中心词是哪个
        for sample in train_data:
            src, tgt = sample['source'], sample['target']
            # 只处理长度一致的替换例子，保证一一对应
            if len(src) != len(tgt):
                continue
            
            # 提取上下文：2字左 + 当前字 + 2字右
            for i in range(len(src)):
                left2 = src[max(0, i-3):i]
                ch    = src[i]
                right2= src[i+1:i+4]
                ctx = left2 + ch + right2 # 上下文
                
                contexts_all.append(ctx)
                is_err = int(ch != tgt[i])
                detect_labels.append(is_err)
                if is_err:
                    contexts_err.append(ctx)
                    correct_labels.append(tgt[i])

        # -- 2. 特征化 -- #
        # 用 char‑ngram TF‑IDF
        self.vectorizer = TfidfVectorizer(
            analyzer='char', ngram_range=(1,3), max_features=70
        )
        X_all = self.vectorizer.fit_transform(contexts_all)
        y_all = np.array(detect_labels)

        # 划分训练/验证集 用于检测器
        X_tr, X_va, y_tr, y_va = train_test_split(
            X_all, y_all, test_size=0.1, random_state=42
        )
        print("\n[Finish context representation...]")
        
        
        """ 
        # 标准化（对稀疏 tf-idf 通常略过）
        self.feature_scaler = StandardScaler(with_mean=False)
        X_train = self.feature_scaler.fit_transform(X_train)
        X_val   = self.feature_scaler.transform(X_val)
        print("\n[Finish Standardization ... ]")
        """

        # -- 3. 训练检测模型 -- #
        # 出现了类别不平衡问题，基本都是label = 1的正确样本在其中。必须使用class_weight='balanced'
        self.detector_model = LogisticRegression(
            max_iter=1000, solver='saga', n_jobs=-1, class_weight='balanced'
        )
        self.detector_model.fit(X_tr, y_tr)
        va_pred = self.detector_model.predict(X_va)
        print(f"[ML-Detect] val acc: {accuracy_score(y_va, va_pred):.4f}")

        print("\n[Finish Detection model Training ... ]")


        """# 训练逻辑回归多分类模型
        from sklearn.linear_model import SGDClassifier
        # SGDClassifier(loss='log'), 随机梯度下降, 分批训练，内存友好、速度快。
        self.ml_model = SGDClassifier(
            loss='log_loss',        # 等价于 logistic regression
            max_iter=20,        
            tol=None,          
            n_jobs=-1
        )"""
        
        
        # -- 4. 训练纠正模型 -- #
        if contexts_err:
            X_err = self.vectorizer.transform(contexts_err)
            y_err = np.array(correct_labels)
            X_tr2, X_va2, y_tr2, y_va2 = train_test_split(
                X_err, y_err, test_size=0.1, random_state=42
            )
            self.corrector_model = LogisticRegression(
                max_iter=1000, solver='saga', multi_class='multinomial', n_jobs=-1
            )
            self.corrector_model.fit(X_tr2, y_tr2)
            corr_pred = self.corrector_model.predict(X_va2)
            print(f"[ML-Correct] val accuracy: {accuracy_score(y_va2, corr_pred):.4f}")
        else:
            print("No error samples to train corrector_model.")
    
        print("\n[Finish Corrction model Training ... ]")



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
        
        if self.detector_model is None or self.corrector_model is None or self.vectorizer is None:
            return text

        corrected = list(text)
        contexts: List[str] = []
        for i in range(len(text)):
            left2 = text[max(0, i-2):i]
            ch    = text[i]
            right2= text[i+1:i+3]
            contexts.append(left2 + ch + right2)

        X_test = self.vectorizer.transform(contexts)
        detect_pred = self.detector_model.predict(X_test)
        corr_pred   = self.corrector_model.predict(X_test)
        
        flag = False
        for i, is_err in enumerate(detect_pred):
            if is_err:
                flag = True
                # 只有检测为错，才应用纠正模型
                corrected[i] = corr_pred[i]
        
        
        # print(flag)
        if flag == True:
            print("++++++", text, "\n")
            print("======", ''.join(corrected), "\n")
        
        
        return ''.join(corrected)
