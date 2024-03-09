# models.py

import numpy as np
import torch
import torch.nn as nn
from transformer import *




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



# testing phase !!!
class NeuralLanguageModel(LanguageModel):
    def __init__(self, trained_Transformer, chunk_size):
        self.model = trained_Transformer # finish training in train_lm
        self.chunk_size = chunk_size
        

    def get_next_char_log_probs(self, context):
        # assume input context is preprocessed into length below chunk_size
        if len(context) == 0:
            context = " "
        elif len(context) > self.chunk_size:
            context = context[-self.chunk_size:]

        prediction = self.model(context)
        res = prediction.detach().numpy()
        return res[ len(res)-1 ]


    def get_log_prob_sequence(self, next_chars, context):
        raise Exception("Implement me")

# 需要完成的任务：
# 1. embedding：从string -> int index -> nn.Embedding 
# 2. model: Transformer（使用库函数 or Part 1中已实现的），调用nn的库函数Transformer
# 3. forward: 前向传播，获得model的输出 

# training phase !!!
class Transformer(nn.Module):
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
        self.vocab_size = len(vocab_index)
        # 1.2 convert int -> embedding (with dimension d_model)
        self.i2e_index = nn.Embedding(self.vocab_size, d_model)
        self.final_embedding_layer = PositionalEncoding(d_model=d_model, num_positions=chunk_size)

        # 2. model: 给TransformerEncoder的输入应该呈形(chunk_size, batch_size, d_model)
        self.model_layer = nn.TransformerEncoderLayer(d_model = d_model, \
            nhead = num_head, dim_feedforward = 4*d_model)
        self.tran_model = nn.TransformerEncoder(self.model_layer, num_layers=num_layers)

        # add: output log probability
        self.convert_to_output = nn.Linear(d_model, self.vocab_size) # output size = self.vocab_size (27 classes)
        self.softmax = torch.nn.LogSoftmax(dim=1)

        # mask: use when call self.model \\\ i.e output_tensor = transformer_encoder(input_tensor, mask=mask_tensor)
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
        int_embedding = np.array([self.s2i_index.index_of(char) for char in context])
        final_embedding = self.final_embedding_layer(self.i2e_index(torch.LongTensor(int_embedding)))

        # 2. compute result 
        final_embedding = final_embedding.reshape((20,1,100)) # mimic dimension when using batch
        temp_output = self.tran_model(final_embedding, self.mask_tensor) # call transformer & mask 
        
        # 3. convert output
        final_output = self.softmax(self.convert_to_output(temp_output))
        return final_output

def text_chunking(text, chunk_size):
    """
    Function: Chunk the input text -> several specific size of texts 
    Tip: overload space and use that as the start-of-sequence character
    """
    chunks = [list(" " + text[i:i + chunk_size-1]) for i in range(0, len(text), chunk_size)]
    for chunk in chunks:
        while len(chunk) < chunk_size:
            chunk.append(' ')
    return chunks

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
    model = Transformer(vocab_index=vocab_index, chunk_size=chunk_size, \
        d_model=d_model, num_head=num_head, num_layers=num_layers)
    model.zero_grad()
    model.train() # 继承的nn.Module,在训练模型时候，需要调.train()，让子模块全部转到训练状态
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    num_epochs = 5
    for t in range(0, num_epochs):
        # You can use batching if you'd like
        loss_function = nn.NLLLoss() # cross extropy for longtensor type
        count = 0
        chunks_list = text_chunking(train_text, chunk_size)
        chunk_idxs = [i for i in range(0, len(chunks_list))]
        random.seed(t)
        random.shuffle(chunk_idxs)
        for ex_idx in chunk_idxs:
            current_context = chunks_list[ex_idx]

            # padding = torch.LongTensor([26])
            # input_tensor = torch.cat((padding,input_tensor[0:-1]))
            log_probs = model(current_context) # 继承了nn.Module时，直接调用model(input)就可以直接得到模型输出！！！
            log_probs = torch.Tensor(log_probs).squeeze()
            
            # BUG!!! log_probs全是0？？梯度根本没法更新！！
            input_indexed = np.array([vocab_index.index_of(ci) for ci in current_context])
            expect_tensor = torch.Tensor(input_indexed).long()
            
            loss = loss_function(log_probs, expect_tensor)
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

            
            
            