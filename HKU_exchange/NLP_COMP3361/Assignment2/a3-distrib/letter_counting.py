# letter_counting.py

import argparse
import json
import time
import numpy as np
from utils import *
from transformer import *

####################################################
# DO NOT MODIFY THIS FILE IN YOUR FINAL SUBMISSION #
####################################################


def _parse_args():
    """
    Command-line arguments to the system. --model switches between the main modes you'll need to use. The other arguments
    are provided for convenience.
    :return: the parsed args bundle
    """
    parser = argparse.ArgumentParser(description='lm.py')
    parser.add_argument('--task', type=str, default='BEFORE', help='task to run (BEFORE or BEFOREAFTER)')
    parser.add_argument('--train', type=str, default='data/lettercounting-train.txt', help='path to train examples')
    parser.add_argument('--dev', type=str, default='data/lettercounting-dev.txt', help='path to dev examples')
    parser.add_argument('--output_bundle_path', type=str, default='classifier-output.json', help='path to write the results json to (you should not need to modify)')
    args = parser.parse_args()
    return args


# 读入文件，返回一个list。其中每个元素都是一个string（去掉了\n滴（不包含最后一个token））
def read_examples(file):
    """
    :param file:
    :return: A list of the lines in the file, each exactly 20 characters long
    """
    all_lines = []
    for line in open(file):
        all_lines.append(line[:-1]) # eat the \n
    print("%i lines read in" % len(all_lines))
    return all_lines


# 处理一个str（train或dev中）。返回本位置前 or 整个列表中出现的次数-1 ！【基于规则来生成label】
def get_letter_count_output(input: str, count_only_previous: bool=True) -> np.array:
    """
    :param input: The string
    :param count_only_previous: True if we should only count previous occurrences, False for all occurrences
    :return: the output for the letter-counting task as a numpy array of 0s, 1s, and 2s
    """
    output = np.zeros(len(input)) # 默认出现次数是0
    for i in range(0, len(input)):
        if count_only_previous: # 只计算当前位置之前token出现的次数（切片自动排除自己）
            output[i] = min(2, len([c for c in input[0:i] if c == input[i]]))
        else: # 计算出现的总次数-1（不包含自己）
            output[i] = min(2, len([c for c in input if c == input[i]]) - 1)  # count all *other* instances of input[i]
    return output


if __name__ == '__main__':
    start_time = time.time()
    args = _parse_args()
    print(args)

    # Constructs the vocabulary: lowercase letters a to z and space
    vocab = [chr(ord('a') + i) for i in range(0, 26)] + [' '] # 27个字符，26个小写字母+空格
    # tip：此时是先转换成ASCII码，再转成character。不用把a-z手动全写一遍啦
    vocab_index = Indexer()
    # 构建字符 - 整数索引的映射字典，存在类属性中
    for char in vocab:
        vocab_index.add_and_get_index(char)
    # 由于是第一次调用，所有vocab中的元素都没有构建双射过，所以有一个隐藏参数add，默认是True
    # print(vocab_index.objs_to_ints)
    # {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 
    # 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 
    # 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, ' ': 26}

    print(repr(vocab_index))

    # 【补】
    # 在 Python 中要将某一类型的变量或者常量转换为字符串对象通常有两种方法，即str() 或者 repr()
    # str()和repr()区别：
    #   函数str( )将其转化成为适于人阅读的前端样式文本
    #   函数repr(object)将对象转化为供解释器读取的形式。返回一个对象的 string 格式。

    count_only_previous = True if args.task == "BEFORE" else False

    # Constructs and labels the data
    train_exs = read_examples(args.train)
    # 真正的input, label。input(处理成原始input，indexed的input，tensor的input，output和tensor)
    train_bundles = \
        [LetterCountingExample(l, get_letter_count_output(l, count_only_previous), vocab_index) \
            for l in train_exs]
    
    dev_exs = read_examples(args.dev)
    dev_bundles = \
        [LetterCountingExample(l, get_letter_count_output(l, count_only_previous), vocab_index) \
             for l in dev_exs]

    model = train_classifier(args, train_bundles, dev_bundles)

    # 【？】train model的时候，传入dev的信息干什么？
    # 难道是train、dev的信息都train，之后再只在dev上检验一下fitting的程度？
    # 难道不是只用train.txt的信息，dev.txt验证fitting程度后，再把两个数据集同时作为training data来train？

    # Decodes the first 5 dev examples to display as output
    # 此时do_plot_attn设置成True还是有问题的，不论attention返还的是softmax后的，还是乘矩阵V的
    decode(model, dev_bundles[0:5], do_print=True, do_plot_attn=True)
    # Decodes 100 training examples and the entire dev set (1000 examples)
    print("Training accuracy (100 exs):")
    decode(model, train_bundles[0:100])
    print("Dev accuracy (whole set):")
    decode(model, dev_bundles)
    end_time = time.time()
    print("Duration: {0}s".format(end_time-start_time))

"""
10000 lines read in
1000 lines read in
INPUT 0: heir average albedo
GOLD 0: array([0, 2, 0, 1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 2, 0, 0, 2, 0, 0, 2])
PRED 0: array([0, 2, 0, 1, 2, 1, 0, 2, 1, 1, 0, 2, 2, 1, 0, 0, 2, 0, 0, 2],
      dtype=int64)
INPUT 1: ed by rank and file
GOLD 1: array([1, 1, 2, 0, 0, 2, 0, 1, 1, 0, 2, 1, 1, 1, 2, 0, 0, 0, 1, 2])
PRED 1: array([2, 1, 2, 0, 0, 2, 0, 2, 1, 0, 2, 2, 1, 1, 2, 0, 1, 0, 2, 2],
      dtype=int64)
INPUT 2: s can also extend in
GOLD 2: array([1, 2, 0, 1, 2, 2, 1, 0, 1, 0, 2, 1, 0, 0, 1, 2, 0, 2, 0, 2])
PRED 2: array([1, 2, 0, 2, 2, 2, 1, 0, 1, 0, 2, 2, 0, 0, 2, 2, 0, 2, 1, 2],
      dtype=int64)
INPUT 3: erages between nine
GOLD 3: array([2, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2])
PRED 3: array([2, 0, 1, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 1, 2, 2, 2],
      dtype=int64)
INPUT 4:  that civilization n
GOLD 4: array([2, 2, 0, 1, 2, 2, 0, 2, 0, 2, 0, 2, 0, 1, 2, 2, 0, 1, 2, 1])
PRED 4: array([2, 2, 0, 1, 2, 2, 0, 2, 0, 2, 0, 2, 0, 1, 2, 2, 0, 1, 2, 1],
      dtype=int64)
Accuracy: 86 / 100 = 0.860000
Training accuracy (100 exs):
Accuracy: 1806 / 2000 = 0.903000
Dev accuracy (whole set):
Decoding on a large number of examples (1000); not printing or plotting
Accuracy: 17702 / 20000 = 0.885100
Duration: 408.08643341064453s
"""

"""
INPUT 0: heir average albedo
GOLD 0: array([0, 2, 0, 1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 2, 0, 0, 2, 0, 0, 2])
PRED 0: array([0, 2, 0, 1, 2, 2, 0, 2, 1, 2, 0, 2, 2, 2, 0, 0, 2, 0, 0, 2],
      dtype=int64)
INPUT 1: ed by rank and file
GOLD 1: array([1, 1, 2, 0, 0, 2, 0, 1, 1, 0, 2, 1, 1, 1, 2, 0, 0, 0, 1, 2])
PRED 1: array([1, 1, 2, 0, 0, 2, 0, 1, 1, 0, 2, 1, 1, 1, 2, 0, 0, 0, 1, 2],
      dtype=int64)
INPUT 2: s can also extend in
GOLD 2: array([1, 2, 0, 1, 2, 2, 1, 0, 1, 0, 2, 1, 0, 0, 1, 2, 0, 2, 0, 2])
PRED 2: array([1, 2, 0, 1, 2, 2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 2, 0, 2, 0, 2],
      dtype=int64)
INPUT 3: erages between nine
GOLD 3: array([2, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2])
PRED 3: array([2, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2],
      dtype=int64)
INPUT 4:  that civilization n
GOLD 4: array([2, 2, 0, 1, 2, 2, 0, 2, 0, 2, 0, 2, 0, 1, 2, 2, 0, 1, 2, 1])
PRED 4: array([2, 2, 0, 1, 2, 2, 0, 2, 0, 2, 0, 2, 0, 1, 2, 2, 0, 1, 2, 1],
      dtype=int64)
Accuracy: 99 / 100 = 0.990000
Training accuracy (100 exs):
Accuracy: 1923 / 2000 = 0.961500
Dev accuracy (whole set):
Decoding on a large number of examples (1000); not printing or plotting
Accuracy: 19124 / 20000 = 0.956200
Duration: 440.35349011421204s
"""