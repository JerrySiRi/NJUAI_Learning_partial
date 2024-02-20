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


def get_letter_count_output(input: str, count_only_previous: bool=True) -> np.array:
    """
    :param input: The string
    :param count_only_previous: True if we should only count previous occurrences, False for all occurrences
    :return: the output for the letter-counting task as a numpy array of 0s, 1s, and 2s
    """
    output = np.zeros(len(input))
    for i in range(0, len(input)):
        if count_only_previous:
            output[i] = min(2, len([c for c in input[0:i] if c == input[i]]))
        else:
            output[i] = min(2, len([c for c in input if c == input[i]]) - 1)  # count all *other* instances of input[i]
    return output


if __name__ == '__main__':
    start_time = time.time()
    args = _parse_args()
    print(args)

    # Constructs the vocabulary: lowercase letters a to z and space
    vocab = [chr(ord('a') + i) for i in range(0, 26)] + [' ']
    vocab_index = Indexer()
    for char in vocab:
        vocab_index.add_and_get_index(char)
    print(repr(vocab_index))

    count_only_previous = True if args.task == "BEFORE" else False

    # Constructs and labels the data
    train_exs = read_examples(args.train)
    train_bundles = [LetterCountingExample(l, get_letter_count_output(l, count_only_previous), vocab_index) for l in train_exs]
    dev_exs = read_examples(args.dev)
    dev_bundles = [LetterCountingExample(l, get_letter_count_output(l, count_only_previous), vocab_index) for l in dev_exs]

    model = train_classifier(args, train_bundles, dev_bundles)
    # Decodes the first 5 dev examples to display as output
    decode(model, dev_bundles[0:5], do_print=True, do_plot_attn=True)
    # Decodes 100 training examples and the entire dev set (1000 examples)
    print("Training accuracy (100 exs):")
    decode(model, train_bundles[0:100])
    print("Dev accuracy (whole set):")
    decode(model, dev_bundles)
