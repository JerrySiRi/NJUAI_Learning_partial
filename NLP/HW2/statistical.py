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

            # Count unigrams (single characters)
            for char in text:
                self.unigram_counts[char] += 1

            # TODO Count bigrams, trigrams, and 4-grams

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
            f"{len(self.bigram_counts)} bigrams, and {len(self.trigram_counts)} trigrams."
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

        # TODO 完成ml方法实现，可选择不同的文本编码方式、不同的特征提取和不同的模型, 推荐先使用一个模型检测，再使用一个模型来纠错。
        # 可以先将训练数据分为训练集和验证集，分别检测两个模型的效果，并调参
        # 可以使用数据增强或者预训练的词向量来提高模型的准确性
        return

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
        elif self.method == 'ml' and SKLEARN_AVAILABLE and self.ml_model is not None:
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
            left_context = text[max(0, i - 2) : i]
            right_context = text[i + 1 : min(len(text), i + 3)]
            context = left_context + '_' + right_context

            # Check if we have seen this character in this context before
            if (char, context) in self.confusion_matrix and self.confusion_matrix[(char, context)]:
                # Get the most common correction for this character in this context
                correction = self.confusion_matrix[(char, context)].most_common(1)[0][0]
                corrected_text[i] = correction
                continue

            # If no specific context match, check general confusion matrix
            if (char, '') in self.confusion_matrix and self.confusion_matrix[(char, '')]:
                # Get the most common correction for this character
                correction = self.confusion_matrix[(char, '')].most_common(1)[0][0]
                # Only apply if it's a common error
                if self.confusion_matrix[(char, '')][correction] > 2:
                    corrected_text[i] = correction
                    continue

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

                # Try all candidates and find the one with highest probability
                best_score = -float('inf')
                best_char = char

                for candidate in candidates:
                    # Skip the original character
                    if candidate == char:
                        continue

                    # Calculate interpolated score using all n-gram models
                    score = 0

                    # Unigram probability (with smoothing)
                    unigram_prob = (self.unigram_counts.get(candidate, 0) + 1) / (
                        sum(self.unigram_counts.values()) + len(self.unigram_counts)
                    )
                    score += self.lambda_1 * unigram_prob

                    # TODO Bigram, trigram, and 4-gram probabilities

                    if score > best_score:
                        best_score = score
                        best_char = candidate

                # Calculate score for the original character
                original_score = 0

                # Unigram probability
                original_unigram_prob = (self.unigram_counts.get(char, 0) + 1) / (
                    sum(self.unigram_counts.values()) + len(self.unigram_counts)
                )
                original_score += self.lambda_1 * original_unigram_prob

                # Bigram probabilities
                if len(left_context) > 0:
                    original_bigram_left = left_context[-1] + char
                    original_bigram_left_prob = (self.bigram_counts.get(original_bigram_left, 0) + 1) / (
                        self.unigram_counts.get(left_context[-1], 0) + len(self.unigram_counts)
                    )
                    original_score += self.lambda_2 * original_bigram_left_prob

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
        return text
