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
        # 常见【字】被混淆了，a:b，a经常被混淆成b
        self.confusion_pairs = {}
        
        # Punctuation rules
        # 标点符号
        self.punctuation_rules = {}
        
        # Grammar rules
        # 语法规则
        self.grammar_rules = {}
        
        # Common word pairs (for word-level correction)
        # 常见【词】被混淆了，ab:ac, ab经常被混淆成ac
        self.word_confusion = {}
        
        # Quantifier-noun pairs (for measure word correction)
        # 量词名词对
        self.quantifier_noun_pairs = {}
        # or else



    def train(self, train_data: List[Dict[str, Any]]) -> None:
        """
        【Extract rules】 from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO 完成规则方法的实现，可以参考如下的方法，或者自行设计
        # 单下划线：内部方法，不推荐外部访问，但其实并没有强制私有化。
        # 双下划线：私有方法，会触发 Python 的名称改写（Name Mangling）机制。
        
        self._extract_confusion_pairs(train_data)
        self._extract_punctuation_rules(train_data)
        self._extract_grammar_rules(train_data)
        self._extract_word_confusion(train_data)

    def _extract_confusion_pairs(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract 【character confusion pairs】 from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # Extract character-level confusion pairs from error examples
        for sample in train_data:
            if sample['label'] == 1:  # Only for sentences with errors
                source = sample['source']
                target = sample['target']
                
                # 【弱假设】假设长度一样只有对应的character出现了混淆（替换）
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
                            
                            # 某一个source，可能会有很多种“混淆”方式，都记录下来统计频率 
                            self.confusion_pairs[s_char][t_char] += 1

        # Filter confusion pairs to keep only the 【most common ones】
        filtered_pairs = {}
        for wrong_char, corrections in self.confusion_pairs.items():
            # Keep only corrections that appear at least twice
            common_corrections = {correct: count for correct, count in corrections.items() if count >= 2}
            if common_corrections:
                filtered_pairs[wrong_char] = common_corrections

        # print(filtered_pairs)
        self.confusion_pairs = filtered_pairs

    # 【补充思考到报告中，使用/不使用Levenshtein还是有很大差别的】
    # 0.0013 -> 0.0102
    def _extract_punctuation_rules(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract 【punctuation correction】 rules from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        
        # TODO
        # 不能只做位置对比，如果发生了删除/插入，source和target发生错位，匹配统计出来没有任何意义。
        
        """
        Extract punctuation correction rules using aligned character operations.
        """
        punctuation_chars = set("，。！？；：（）【】《》“”‘’")
        punctuation_pairs = defaultdict(lambda: defaultdict(int))

        for sample in train_data:
            if sample['label'] != 1:
                continue

            src = sample['source']
            tgt = sample['target']

            # 使用 Levenshtein 分析编辑操作（替换/插入/删除）
            try:
                import Levenshtein
                edits = Levenshtein.opcodes(src, tgt)
            except Exception as e:
                continue

            for tag, i1, i2, j1, j2 in edits:
                if tag == 'replace':
                    for s_char, t_char in zip(src[i1:i2], tgt[j1:j2]):
                        if s_char in punctuation_chars and t_char in punctuation_chars:
                            punctuation_pairs[s_char][t_char] += 1

        # 筛选高频替换规则（可调阈值）
        self.punctuation_rules = {
            wrong_punc: {
                right_punc: count
                for right_punc, count in replacements.items()
                if count >= 2
            }
            for wrong_punc, replacements in punctuation_pairs.items()
            if any(count >= 2 for count in replacements.values())
        }
        print(self.punctuation_rules)
        
    
    # F0.5 Score: 0.0069。引入jieba好像还没有没引入时候效果好呀。之前是0.0102
    # 【补充思考到报告中】
    def _extract_grammar_rules(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract 【grammar correction rules】 from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO
        """
        使用词性（POS）模式从训练数据中提取通用语法纠错规则。

        规则格式：
            (错误字, 左词性, 当前词性, 右词性) → 正确字
        """
        
        import jieba.posseg as pseg
        pos_grammar_rules = defaultdict(lambda: defaultdict(int))
        
        for sample in train_data:
            if sample['label'] != 1:
                continue

            src = sample['source']
            tgt = sample['target']

            # 仅考虑长度相同（替换类错误）
            if len(src) != len(tgt):
                continue

            # 词性标注
            words = list(pseg.cut(src))
            char_pos = []
            for word, flag in words:
                char_pos.extend([flag] * len(word))

            if len(char_pos) != len(src):
                continue  # 保护性跳过

            for i, (s_char, t_char) in enumerate(zip(src, tgt)):
                if s_char == t_char:
                    continue  # 无需纠错

                left_pos = char_pos[i - 1] if i > 0 else 'NONE'
                mid_pos = char_pos[i]
                right_pos = char_pos[i + 1] if i < len(src) - 1 else 'NONE'

                pattern = (s_char, left_pos, mid_pos, right_pos)
                pos_grammar_rules[pattern][t_char] += 1

        # 筛选高频规则
        self.grammar_rules = {
            pattern: {
                correct_char: count
                for correct_char, count in candidates.items()
                if count >= 10
            }
            for pattern, candidates in pos_grammar_rules.items()
            if any(count >= 10 for count in candidates.values())
        }

        print(self.grammar_rules)

         
        

    def _extract_word_confusion(self, train_data: List[Dict[str, Any]]) -> None:
        """
        Extract word-level confusion pairs from the training data.

        Args:
            train_data: List of dictionaries containing the training data.
        """
        # TODO
        if not JIEBA_AVAILABLE:
            print("jieba not available, skipping word confusion extraction.")
            return

        word_pairs = defaultdict(lambda: defaultdict(int))

        for sample in train_data:
            if sample['label'] == 1:
                src, tgt = sample['source'], sample['target']
                src_words = list(jieba.cut(src))
                tgt_words = list(jieba.cut(tgt))

                for sw, tw in zip(src_words, tgt_words):
                    if sw != tw and abs(len(sw) - len(tw)) <= 2:
                        word_pairs[sw][tw] += 1

        self.word_confusion = {
            w: {tw: cnt for tw, cnt in corrections.items() if cnt >= 2}
            for w, corrections in word_pairs.items()
            if any(cnt >= 2 for cnt in corrections.values())
        }


    def correct(self, text: str) -> str:
        """
        【Apply】 rule-based correction to the input text.

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
        Correct 【punctuation errors】 in the text.

        Args:
            text: Input text.

        Returns:
            Text with corrected punctuation.
        """
        # TODO
        corrected = []
        for ch in text:
            if ch in self.punctuation_rules:
                # 取最常出现的替换符号
                replacement = max(self.punctuation_rules[ch].items(), key=lambda x: x[1])[0]
                corrected.append(replacement)
            else:
                corrected.append(ch)
        return ''.join(corrected)

    def _correct_confusion_chars(self, text: str) -> str:
        """
        Correct 【character confusion errors】 in the text.

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

                # ---------------------- 手动处理一些困难情况 ---------------------- # 
                
                # --- 【规则1】 --- #
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
                
                # --- 【规则2】 --- #
                # For other confusions, apply a simpler rule
                elif char in ['在', '再'] and correct_char in ['再', '在']:
                    # '在' typically indicates location, '再' typically indicates repetition or future action
                    if i < len(text) - 1 and text[i + 1] in '次遍回':
                        corrected_text[i] = '再'
                    elif i > 0 and text[i - 1] in '正将':
                        corrected_text[i] = '在'
                
                # # TODO more rules、
                # 自己想确实想不太出来呢 o(╥﹏╥)o
                # --- 【规则3】 --- #
                elif char == '事' and correct_char == '是':
                    if i > 0 and text[i - 1] in '这那他她你' and i < len(text) - 1 and text[i + 1] in '的了啊嘛':
                        corrected_text[i] = '是'

                # --- 【规则4】 --- #
                elif char in ['以', '亦'] and correct_char == '已':
                    if i > 0 and text[i - 1] in '我他她你' and i < len(text) - 1 and text[i + 1] in '经知完成':
                        corrected_text[i] = '已'

                # ------------------------- 统计出来的有信心的情况才做替换 ------------------------ #
                # For other cases, only correct if we're very confident
                # This is a placeholder for more sophisticated rules
                elif self.confusion_pairs[char][correct_char] > 5:  # Arbitrary threshold
                    corrected_text[i] = correct_char

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
        if not self.grammar_rules:
            return text
        
        try:
            import jieba.posseg as pseg
        except ImportError:
            print("jieba.posseg not available, skipping POS-based grammar correction.")
            return text

        words = list(pseg.cut(text))
        char_pos = []
        for word, flag in words:
            char_pos.extend([flag] * len(word))

        if len(char_pos) != len(text):
            return text  
        corrected = list(text)
        for i, char in enumerate(text):
            left_pos = char_pos[i - 1] if i > 0 else 'NONE'
            mid_pos = char_pos[i]
            right_pos = char_pos[i + 1] if i < len(text) - 1 else 'NONE'
            pattern = (char, left_pos, mid_pos, right_pos)
            
            if pattern in self.grammar_rules:
                # 获取最可能的替换字
                replacements = self.grammar_rules[pattern]
                best_replacement = max(replacements.items(), key=lambda x: x[1])[0]
                corrected[i] = best_replacement

        return ''.join(corrected)


    def _correct_word_confusion(self, text: str) -> str:
        """
        Correct word-level confusion errors in the text.

        Args:
            text: Input text.

        Returns:
            Text with corrected words.
        """
        # TODO
        if not JIEBA_AVAILABLE:
            return text

        words = list(jieba.cut(text))
        corrected_words = []

        for w in words:
            if w in self.word_confusion:
                # 使用最高频的替换项
                best = max(self.word_confusion[w].items(), key=lambda x: x[1])[0]
                corrected_words.append(best)
            else:
                corrected_words.append(w)

        return ''.join(corrected_words)

