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
    def __init__(self, vocab_index, chunk_size, d_model, num_head, num_layers):
        raise Exception("Implement me")
        

    def get_next_char_log_probs(self, context):
        raise Exception("Implement me")

    def get_log_prob_sequence(self, next_chars, context):
        raise Exception("Implement me")


class Transformer(torch.nn.Module):
    def __init__(self, vocab_index, chunk_size, d_model, num_head, num_layers):
        """
        vocab_index: indexer to covert string->int
        d_model: input dimension of Transformer
        num_head: multi-head self-attention
        num_layers: layers of Transformer
        num_positions: PositionalEncoding will use it [its value = chunk size]
        """
        super().__init__()

        # 1. Embedding
        # 1.1 convert string -> int  
        self.s2i_index = vocab_index 
        self.vocab_size = len(self.indexer)
        # 1.2 convert int -> embedding (with dimension d_model)
        self.i2e_index = nn.Embedding(self.vocab_size, d_model)
        self.final_embedding_layer = PositionalEncoding(d_model, chunk_size)

        # 2. model: 给TransformerEncoder的输入应该呈形(chunk_size, batch_size, d_model)
        self.model_layer = nn.TransformerEncoderLayer(d_model = d_model, \
            nhead = num_head, dim_feedforward = 4*d_model)
        self.model = nn.TransformerEncoder(self.model_layer, num_layers=num_layers)

        # add: output log probability
        self.convert_to_output = nn.Linear(d_model, self.vocab_size) # output size = self.vocab_size
        self.softmax = torch.nn.LogSoftmax(dim=1)

        # mask: use when call self.model
        # i.e output_tensor = transformer_encoder(input_tensor, mask=mask_tensor)
        self.mask_tensor = torch.zeros(chunk_size, chunk_size, dtype=torch.bool)
        for i in range(0, chunk_size):
            for j in range(i+1, chunk_size):
                self.mask_tensor[i,j] = True
        

    def forward(self, context):
        """
        context: after chunking the original text
        **should reshape to (chunk_size, batch_size, input_dim)
        """
        # 1. embedding
        int_embedding = [self.s2i_index.index_of(char) for char in context]
        final_embedding = self.final_embedding_layer(self.i2e_index(int_embedding))

        # 2. compute result
        temp_output = self.model(final_embedding, self.mask_tensor)
        final_output = self.softmax(self.convert_to_output(temp_output)).detach().numpy()

        # 3. convert output
        output = self.softmax(self.convert_to_output(final_output))
        return output


# 【不可以改参数，会import这个函数来测试的】
def train_lm(args, train_text, dev_text, vocab_index):
    """
    :param args: command-line args, passed through here for your convenience
    :param train_text: train text as a sequence of characters
    :param dev_text: dev text as a sequence of characters
    :param vocab_index: an Indexer of the character vocabulary (27 characters)
    :return: a NeuralLanguageModel instance trained on the given data
    """
    chunk_size = 20
    d_model = 100
    num_head = 4
    num_layers = 3
    Whole_model = NeuralLanguageModel(chunk_size=chunk_size,d_model=d_model,num_head=num_head,num_layers=num_layers)
    model.zero_grad()
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    num_epochs = 4
    for t in range(0, num_epochs):
        random.seed(t)
        # You can use batching if you'd like
        ex_idxs = [i for i in range(0, len(train_text)-chunk_size,chunk_size)]
        random.shuffle(ex_idxs)
        loss_fcn = torch.nn.NLLLoss()
        count=0
        for ex_idx in ex_idxs:
            input = train_text[ex_idx: ex_idx+chunk_size]
            input_indexed = np.array([vocab_index.index_of(ci) for ci in input])
            input_tensor = torch.LongTensor(input_indexed)

            expect_tensor = input_tensor
            padding = torch.LongTensor([26])
            input_tensor = torch.cat((padding,input_tensor[0:-1]))

            l= model(input_tensor)
            loss = loss_fcn(l, expect_tensor)
            loss_val = loss.detach().cpu().numpy()
   

            model.zero_grad()
            loss.backward()
            optimizer.step()

            count = count+1
            if count%50==0:
                print(loss_val)
                print_evaluation(dev_text, NeuralLanguageModel(model, vocab_index, chunk_size), vocab_index, args.output_bundle_path)
                
    model.eval()
    return NeuralLanguageModel(model, vocab_index, chunk_size)
