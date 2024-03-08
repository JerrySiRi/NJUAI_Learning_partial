# models.py

import numpy as np
import torch
import torch.nn as nn
from transformer import *

def text_chunking(text, chunk_size):
    """
    Function: Chunk the input text -> several specific size of texts 
    Tip: overload space and use that as the start-of-sequence character
    """
    chunks = [list(" " + text[i:i + chunk_size]) for i in range(0, len(text), chunk_size)]
    for chunk in chunks:
        while len(chunk) < chunk_size:
            chunk.append(' ')
    return chunks


class LanguageModel(object):

    def get_next_char_log_probs(self, context) -> np.ndarray:
        """
        Returns a log probability distribution over the next characters given a context.
        The log should be base e

        NOTE: You should make sure you call model.eval() to determinize inference here (turns off dropout
        layers in TransformerEncoder).
        :param context: the string context that the LM conditions on
        :return: A numpy vector log P(y | context) where y ranges over the output vocabulary.
        """
        raise Exception("Only implemented in subclasses")


    def get_log_prob_sequence(self, next_chars, context) -> float:
        """
        Scores a bunch of characters following context. That is, returns
        log P(nc1, nc2, nc3, ... | context) = log P(nc1 | context) + log P(nc2 | context, nc1), ...
        The log should be base e

        NOTE: You should make sure you call model.eval() to determinize inference here (turns off dropout
        layers in TransformerEncoder).
        :param next_chars:
        :param context:
        :return: The float probability
        """
        raise Exception("Only implemented in subclasses")


class UniformLanguageModel(LanguageModel):
    def __init__(self, voc_size):
        self.voc_size = voc_size

    def get_next_char_log_probs(self, context):
        return np.ones([self.voc_size]) * np.log(1.0/self.voc_size)

    def get_log_prob_sequence(self, next_chars, context):
        return np.log(1.0/self.voc_size) * len(next_chars)

# 需要完成的任务：
# 1. embedding：从string -> int index -> nn.Embedding 
# 2. model: Transformer（使用库函数 or Part 1中已实现的），调用nn的库函数Transformer
# 3. forward: 前向传播，获得model的输出 

class NeuralLanguageModel(LanguageModel):
    def __init__(self, vocab_index, d_model, num_head, num_layers, num_positions):
        """
        vocab_index: indexer to covert string->int
        d_model: input dimension of Transformer
        num_head: multi-head self-attention
        num_layers: layers of Transformer
        num_positions: PositionalEncoding will use it [its value = chunk size]
        """
        # mask: shape of attention map is [num_heads, seq_length, seq_length]
        mask_tensor = torch.zeros(seq_length, seq_length, dtype=torch.bool)
        mask_tensor[-2:, :] = True 
        
        # 1.1 convert string -> int  
        self.s2i_index = vocab_index 
        self.vocab_size = len(self.indexer)
        # 1.2 convert int -> embedding (with dimension d_model)
        self.i2e_index = nn.Embedding(self.vocab_size, d_model)
        self.final_embedding_layer = PositionalEncoding(d_model, num_positions)
        # 2. model: 给TransformerEncoder的输入应该呈形(seq_length, batch_size, input_dim)
        self.model_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=num_head)
        self.model = nn.TransformerEncoder(self.model_layer, num_layers=num_layers)
        # add: output log probability
        self.convert_to_output = nn.Linear(d_model, self.vocab_size) # output size = self.vocab_size
        self.softmax = nn.LogSoftmax()
        


    def get_next_char_log_probs(self, context):
        """
        context: after chunking the original text
        **should reshape to (seq_length, batch_size, input_dim)
        """
        # 1. embedding
            # 1.1 string -> int
        int_index = [self.s2i_index.index_of(char) for char in context]
            # 1.2 int -> embedding
        partial_embedding = self.i2e_index(int_index)
        final_embedding = self.final_embedding_layer(partial_embedding)
        # 2. model


        raise Exception("Implement me")

    def get_log_prob_sequence(self, next_chars, context):
        raise Exception("Implement me")

# 【不可以改参数，会import这个函数来测试的】
def train_lm(args, train_text, dev_text, vocab_index):
    """
    :param args: command-line args, passed through here for your convenience
    :param train_text: train text as a sequence of characters
    :param dev_text: dev text as a sequence of characters
    :param vocab_index: an Indexer of the character vocabulary (27 characters)
    :return: a NeuralLanguageModel instance trained on the given data
    """
    raise Exception("Implement me")
