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
import Levenshtein


# Try to import optional dependencies
try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False
    print("Warning: jieba not available. Some features will be disabled.")


# --------------------- 依存句法分析 --------------------- # 
from ltp import LTP
# 成分句法分析已经被移除，以下代码使用依存句法分析
# 但是依存句法分析必须用(head, label)来额外训练一个model
# 训练：统计(head -> current word)之间的关系label
# 测试：难道要对每一个
class LTPDependencyParser:
    def __init__(self):
        self.ltp = LTP("LTP/base")

    def get_dependency_tags(self, text: str) -> List[str]:
        output = self.ltp.pipeline([text], tasks=["cws", "dep"], return_dict=True)
        # 做分词，example: ['他', '的', '回答', '很', '精彩', '。']
        words = output["cws"][0]
        # 做依存句法分析，example: {'head': [3, 1, 5, 5, 0, 5], 'label': ['ATT', 'RAD', 'SBV', 'ADV', 'HED', 'WP']}
        # - `head` 是表示每个词的“父节点”的索引
        # - `label` 是依存关系的标签，如 `'ATT'`（属性），`'SBV'`（主谓关系），`'HED'`（谓词）
        head = output["dep"][0]['head'] # 根节点
        rels = output["dep"][0]['label']  # 直接是每个词的依存关系标签，如 ['ATT', 'SBV', 'ADV'...]
        
        # 将词性标签展开为字符级标签
        labels = []
        for word, head, rel in zip(words, head, rels):
            labels.append((head * len(word), rel * len(word)))
        if len(labels) != len(text):
            raise ValueError("标签长度与字符长度不一致")
        return labels


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
        # 语法规则，存储做pos时的结果
        self.grammar_rules = {} 
        # 依存句法分析    
        self.dependency_parser = LTPDependencyParser()     
        
        
        # Common word pairs (for word-level correction)
        # 常见【词】被混淆了，ab:ac, ab经常被混淆成ac
        self.word_confusion = {}
        
        # Quantifier-noun pairs (for measure word correction)
        # 量词名词对
        self.quantifier_noun_pairs = {}
        # or else


    def train(self, train_data: List[Dict[str, Any]], grammar = "pos") -> None:
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
        
        if grammar == "pos":
            self._extract_grammar_rules_pos(train_data)
        elif grammar == "dep":
            self._extract_grammar_rules_dep(train_data)
            
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
            common_corrections = {correct: count for correct, count in corrections.items() if count >= 5}
            if common_corrections:
                filtered_pairs[wrong_char] = common_corrections

        # print(filtered_pairs)
        
        self.confusion_pairs = filtered_pairs
        print(f"\n[Character Grammar] 规则数量: {len(self.confusion_pairs)}")
        print(self.confusion_pairs)


    # 【补充思考到报告中，使用/不使用Levenshtein还是有很大差别的】
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
            if sample['label'] != 1: # 只对error分析
                continue

            src = sample['source']
            tgt = sample['target']

            # 使用 Levenshtein 分析编辑操作（替换/插入/删除）
            try:
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
        print(f"\n[Punctation Grammar] 规则数量: {len(self.punctuation_rules)}")
        print(self.punctuation_rules)
        
    # 法一：属于基于词性（POS）的语法模式抽取方法
    # 规则格式：
    # (错误字, 左词性, 当前词性, 右词性) → 正确字
    
    # 法二：使用 Levenshtein.opcodes(src, tgt) 来对齐 source 和 target
    #       并结合 成分句法分析（constituent parsing） 提取语法错误规则
    # 不能只匹配长度一样的内容，训练集里边没有这样的样本。。
    # -- LTP库：现在的库已经不支持了
    # -- Transformer：huggingface中实现依存句法分析的model
    
    def _extract_grammar_rules_dep(self, train_data: List[Dict[str, Any]]) -> None:
        
        grammar_rules = defaultdict(lambda: defaultdict(int))
        parser = self.dependency_parser
        self.count_limit = 5

        for sample in train_data:
            if sample['label'] != 1:
                continue
            src = sample['source']
            tgt = sample['target']
            try:
                dep_labels = parser.get_dependency_tags(src)
            except Exception as e:
                print("依存分析失败：", e)
                continue
            if len(dep_labels) != len(src):
                print("长度不一致，跳过")
                continue
            
            try:
                edits = Levenshtein.opcodes(src, tgt)
            except Exception:
                continue
            
            for tag, i1, i2, j1, j2 in edits:
                if tag == 'replace':
                    for si, ti in zip(range(i1, i2), range(j1, j2)):
                        if si >= len(src) or ti >= len(tgt):
                            continue
                        s_char = src[si]
                        t_char = tgt[ti]
                        label = dep_labels[si]
                        pattern = (s_char, label)
                        grammar_rules[pattern][t_char] += 1

        self.grammar_rules = {
            pattern: {
                correct: count for correct, count in candidates.items() if count >= 5
            }
            for pattern, candidates in grammar_rules.items()
            if any(count >= self.count_limit for count in candidates.values())
        }

        print(f"\n[Dependency Grammar] 规则数量: {len(self.grammar_rules)}")
        print(f"Config: {self.count_limit}")
        print(self.grammar_rules)
        

    # 当前设置（不计算character confusion)
    # 最优解 F0.5 - 0.2175
    def _extract_grammar_rules_pos(self, train_data: List[Dict[str, Any]]) -> None:
        import jieba.posseg as pseg
        self.length = 2
        self.count_limit = 10
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

                left_pos = char_pos[i - self.length] if i > 0 else 'NONE'
                mid_pos = char_pos[i]
                right_pos = char_pos[i + self.length] if i < len(src) - self.length else 'NONE'

                pattern = (s_char, left_pos, mid_pos, right_pos)
                pos_grammar_rules[pattern][t_char] += 1

        # 筛选高频规则
        self.grammar_rules = {
            pattern: {
                correct_char: count
                for correct_char, count in candidates.items()
                if count >= self.count_limit
            }
            for pattern, candidates in pos_grammar_rules.items()
            if any(count >= self.count_limit for count in candidates.values())
        }
        print(f"\n[POS Grammar] 提取数量: {len(self.word_confusion)}")
        print(f"[Config -] context length: {self.length},count limit: {self.count_limit} ")
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
            if sample['label'] != 1:
                continue

            src, tgt = sample['source'], sample['target']
            src_words = list(jieba.cut(src))
            tgt_words = list(jieba.cut(tgt))

            try:
                ops = Levenshtein.opcodes(' '.join(src_words), ' '.join(tgt_words))
            except Exception as e:
                print("Levenshtein alignment failed:", e)
                continue

            src_ptr, tgt_ptr = 0, 0
            for tag, i1, i2, j1, j2 in ops:
                # Convert i1/i2/j1/j2 from char-based to word-level span index
                src_segment = src_words[src_ptr:src_ptr + (i2 - i1)]
                tgt_segment = tgt_words[tgt_ptr:tgt_ptr + (j2 - j1)]

                if tag == 'replace':
                    for sw, tw in zip(src_segment, tgt_segment):
                        if sw != tw and abs(len(sw) - len(tw)) <= 2:
                            word_pairs[sw][tw] += 1

                src_ptr += (i2 - i1)
                tgt_ptr += (j2 - j1)

        self.word_confusion = {
            w: {tw: cnt for tw, cnt in corrections.items() if cnt >= 2}
            for w, corrections in word_pairs.items()
            if any(cnt >= 2 for cnt in corrections.values())
        }

        print(f"\n[Word Confusion] 提取规则数量: {len(self.word_confusion)}")
        print(self.word_confusion)


    def correct(self, text: str, choice: str) -> str:
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
        corrected = self._correct_grammar(corrected, choice)
        # corrected = self._correct_confusion_chars(corrected)    
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


    def _correct_grammar(self, text: str, choice="pos") -> str:
        """
        Correct grammar errors in the text.

        Args:
            text: Input text.

        Returns:
            Text with corrected grammar.
        """
        # TODO
        
        if choice == "dep":
            try:
                dep_labels = self.dependency_parser.get_dependency_tags(text)
            except Exception as e:
                print("依存分析失败：", e)
                return text

            corrected = list(text)

            for i, (char, dep) in enumerate(zip(text, dep_labels)):
                pattern = (char, dep)
                if pattern in self.grammar_rules:
                    candidates = self.grammar_rules[pattern]
                    if candidates:
                        # 选择频率最高的替换字符
                        best = max(candidates.items(), key=lambda x: x[1])[0]
                        if best != char:
                            corrected[i] = best
            return ''.join(corrected)
    
        elif choice == "pos":
            import jieba.posseg as pseg
            # 获取每个字符的词性（按词扩展）
            words = list(pseg.cut(text))
            char_pos = []
            for word, flag in words:
                char_pos.extend([flag] * len(word))

            if len(char_pos) != len(text):
                # 保护性判断
                return text

            corrected = list(text)
            for i, char in enumerate(text):
                left_pos = char_pos[i - self.length] if i > 0 else 'NONE'
                mid_pos = char_pos[i]
                right_pos = char_pos[i + self.length] if i < len(text) - self.length else 'NONE'

                pattern = (char, left_pos, mid_pos, right_pos)
                if pattern in self.grammar_rules:
                    candidates = self.grammar_rules[pattern]
                    if candidates:
                        best = max(candidates.items(), key=lambda x: x[1])[0]
                        if best != char:
                            corrected[i] = best
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


if __name__ == "__main__":
    parser = LTPDependencyParser()
    labels = parser.get_dependency_tags("他的回答很精彩。")
    print(labels)



