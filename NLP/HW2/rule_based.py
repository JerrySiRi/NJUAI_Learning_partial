#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rule-based corrector for Chinese Text Correction task.
This module implements rule-based methods for correcting errors in Chinese text.
"""

import re
import json
from typing import Dict, List, Tuple, Any, Set
from collections import defaultdict

# Try to import optional dependencies
try:
    import jieba

    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("Warning: jieba not available. Some features will be disabled.")


class RuleBasedCorrector:
    """
    A rule-based corrector for Chinese text.
    """

    def __init__(self):
        """
        Initialize the rule-based corrector.
        """
        # Common confusion pairs (similar characters)
        self.confusion_pairs = {}

        # Punctuation rules
        self.punctuation_rules = {}

        # Grammar rules
        self.grammar_rules = {}

        # Common word pairs (for word-level correction)
        self.word_confusion = {}

        # Quantifier-noun pairs (for measure word correction)
        self.quantifier_noun_pairs = {}

        # or else

    def train(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract rules from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO 完成规则方法的实现，可以参考如下的方法，或者自行设计
        self._extract_confusion_pairs(train_data)
        self._extract_punctuation_rules(train_data)
        self._extract_grammar_rules(train_data)
        self._extract_word_confusion(train_data)

    def _extract_confusion_pairs(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract character confusion pairs from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # Extract character-level confusion pairs from error examples
        for sample in train_data:
            if sample['label'] == 1:  # Only for sentences with errors
                source = sample['source']
                target = sample['target']

                # For character substitution errors (when lengths are equal)
                if len(source) == len(target):
                    for i, (s_char, t_char) in enumerate(zip(source, target)):
                        if s_char != t_char:
                            # Get context (surrounding characters)
                            left_context = source[max(0, i - 2) : i]
                            right_context = source[i + 1 : min(len(source), i + 3)]
                            context = left_context + '_' + right_context

                            # Add to confusion pairs with context
                            if s_char not in self.confusion_pairs:
                                self.confusion_pairs[s_char] = defaultdict(int)
                            self.confusion_pairs[s_char][t_char] += 1

        # Filter confusion pairs to keep only the most common ones
        filtered_pairs = {}
        for wrong_char, corrections in self.confusion_pairs.items():
            # Keep only corrections that appear at least twice
            common_corrections = {correct: count for correct, count in corrections.items() if count >= 2}
            if common_corrections:
                filtered_pairs[wrong_char] = common_corrections

        self.confusion_pairs = filtered_pairs

    def _extract_punctuation_rules(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract punctuation correction rules from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO
        return

    def _extract_grammar_rules(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract grammar correction rules from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO
        return

    def _extract_word_confusion(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract word-level confusion pairs from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO
        return

    def correct(self, text: str) -> str:
        """
        Apply rule-based correction to the input text.

        Args:
            text: Input text to correct.

        Returns:
            Corrected text.
        """
        # Apply different correction rules in sequence
        # TODO 对应规则方法的实现，完成修正部分（可以参考如下的方法，或者自行设计）
        corrected = self._correct_punctuation(text)
        corrected = self._correct_confusion_chars(corrected)
        corrected = self._correct_grammar(corrected)
        corrected = self._correct_word_confusion(corrected)

        return corrected

    def _correct_punctuation(self, text: str) -> str:
        """
        Correct punctuation errors in the text.

        Args:
            text: Input text.

        Returns:
            Text with corrected punctuation.
        """
        # TODO
        return text

    def _correct_confusion_chars(self, text: str) -> str:
        """
        Correct character confusion errors in the text.

        Args:
            text: Input text.

        Returns:
            Text with corrected characters.
        """
        corrected_text = list(text)  # Convert to list for character-by-character editing

        # Check each character for potential confusion
        for i, char in enumerate(text):
            if char in self.confusion_pairs and self.confusion_pairs[char]:
                # Get the most common correction for this character
                correct_char = max(self.confusion_pairs[char].items(), key=lambda x: x[1])[0]

                # Apply some heuristics to decide whether to correct
                # For example, check if the correction makes sense in this context
                # This is a simplified approach; in a real system, more context would be considered

                # For the common confusion of 的/地/得, apply specific rules
                if char == '的' and correct_char in ['地', '得']:
                    # '地' typically follows an adjective and precedes a verb
                    if i > 0 and i < len(text) - 1 and text[i + 1] not in ',.?!，。？！、；：':
                        # Simple check: if followed by a verb-like character, might be '地'
                        if text[i + 1] in '走跑跳跃飞奔跑跳跃飞奔跑跳跃飞奔':
                            corrected_text[i] = '地'

                    # '得' typically follows a verb and precedes an adjective or adverb
                    if i > 0 and i < len(text) - 1 and text[i - 1] not in ',.?!，。？！、；：':
                        # Simple check: if preceded by a verb-like character, might be '得'
                        if text[i - 1] in '说写跑跳走看听闻感觉':
                            corrected_text[i] = '得'

                # For other confusions, apply a simpler rule
                elif char in ['在', '再'] and correct_char in ['再', '在']:
                    # '在' typically indicates location, '再' typically indicates repetition or future action
                    if i < len(text) - 1 and text[i + 1] in '次遍回':
                        corrected_text[i] = '再'
                    elif i > 0 and text[i - 1] in '正将':
                        corrected_text[i] = '在'

                # For other cases, only correct if we're very confident
                # This is a placeholder for more sophisticated rules
                elif self.confusion_pairs[char][correct_char] > 5:  # Arbitrary threshold
                    corrected_text[i] = correct_char

                # TODO more rules

        return ''.join(corrected_text)

    def _correct_grammar(self, text: str) -> str:
        """
        Correct grammar errors in the text.

        Args:
            text: Input text.

        Returns:
            Text with corrected grammar.
        """
        # TODO
        return text

    def _correct_word_confusion(self, text: str) -> str:
        """
        Correct word-level confusion errors in the text.

        Args:
            text: Input text.

        Returns:
            Text with corrected words.
        """
        # TODO
        return text
