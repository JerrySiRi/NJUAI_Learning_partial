# models.py

import numpy as np
import torch
import torch.nn as nn
from transformer import *
from lm import print_evaluation # BUG: 不能相互import *，只相互import各自的一部分（某个函数）还是可以的




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
    def __init__(self, trained_Transformer, vocab_index, chunk_size):
        self.model = trained_Transformer # finish training in train_lm
        self.chunk_size = chunk_size
        self.vocab_index = vocab_index
        

    def get_next_char_log_probs(self, context):
        # assume input context is preprocessed into length below chunk_size
        # TODO: 依据已有的context估计下一个char的log pro
        #print("===char===")
        if type(context) == str:
            context = [self.vocab_index.index_of(char) for char in context]
        chunk_context = context[-self.chunk_size+1: ]
        prediction = self.model(chunk_context)
        res = prediction.detach().numpy()
        # print("---Finish next char log probs---")
        return res[ len(res)-1 ][0] # batch -- squeeze the dimension only have 1 element


    def get_log_prob_sequence(self, next_chars, initial_context):
        # print_evaluation中调用 -- log_prob = lm.get_log_prob_sequence(text, "")
        # context是已经有的序列
        # next_chars是在已经有的序列上，下一个token(从next_chars这个sequence中拿)是他。来算它的概率
        log_sum = 0
        cur_context = initial_context
        if type(initial_context) == str:
            cur_context = [self.vocab_index.index_of(char) for char in initial_context]
        if type(next_chars) == str:
            next_chars = [self.vocab_index.index_of(char) for char in next_chars]
        for acc_index in next_chars:
            cur_context = cur_context[-self.chunk_size+1:] # 防止不断加入超过chunk_size上限
            #print(cur_context)
            dist = self.get_next_char_log_probs(np.array(cur_context))
            log_sum += dist[acc_index]
            cur_context.append(acc_index)
        return log_sum

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
        self.trans_model = nn.TransformerEncoder(self.model_layer, num_layers=num_layers)

        # add: output log probability
        self.convert_to_output = nn.Linear(d_model, self.vocab_size) # output size = self.vocab_size (27 classes)
        self.softmax = torch.nn.LogSoftmax(dim = -1)

       
    def forward(self, indexed_context):
        """
        context: after chunking the original text
        **should reshape to (chunk_size, batch_size, input_dim)
        """
        # 1. embedding
        # int_embedding = np.array([self.s2i_index.index_of(char) for char in context])
        final_embedding = self.final_embedding_layer(self.i2e_index(torch.LongTensor(indexed_context)))

        # 2. mask & compute result 
        # mask: use when call self.model \\\ i.e output_tensor = transformer_encoder(input_tensor, mask=mask_tensor)
        mask_tensor = torch.zeros(len(indexed_context), len(indexed_context), dtype=torch.bool)
        for i in range(0, len(indexed_context)):
            for j in range(i+1, len(indexed_context)):
                mask_tensor[i,j] = True

        final_embedding = final_embedding.reshape((final_embedding.shape[0],1,\
            final_embedding.shape[1])) # imitate dimension when using batch
        temp_output = self.trans_model(final_embedding, mask_tensor) # call transformer & mask 
        
        
        # 3. convert output
        o1 = self.convert_to_output(temp_output)
        # o1 = torch.Tensor(o1).squeeze()
        o2 = self.softmax(o1)
        return o2

def text_chunking_indexed(text, chunk_size, vocab_index, need_whitespace=True):
    """
    Function: Chunk the input text -> several specific size of texts 
    Tip: overload space and use that as the start-of-sequence character
    """
    if need_whitespace == True: # training data
        chunks = [list(" " + text[i:i + chunk_size-1]) for i in range(0, len(text), chunk_size)]
        for chunk in chunks:
            while len(chunk) < chunk_size:
                chunk.append(' ')
    else:# testing data
        chunks = [list(text[i:i + chunk_size]) for i in range(0, len(text), chunk_size)]
        for chunk in chunks:
            while len(chunk) < chunk_size:
                chunk.append(' ')
    
    indexed_chunk = []
    for chunk in chunks:
        int_embedding = np.array([vocab_index.index_of(char) for char in chunk])
        indexed_chunk.append(int_embedding)
    return indexed_chunk


# 【不可以改参数，会import这个函数来测试的】
def train_lm(args, train_text, dev_text, vocab_index):
    """
    :param args: command-line args, passed through here for your convenience
    :param train_text: train text as a sequence of characters
    :param dev_text: dev text as a sequence of characters
    :param vocab_index: an Indexer of the character vocabulary (27 characters)
    :return: a NeuralLanguageModel instance trained on the given data
    """
    chunk_size = 32
    d_model = 100
    num_head = 4
    num_layers = 3
    model = Transformer(vocab_index=vocab_index, chunk_size=chunk_size, \
        d_model=d_model, num_head=num_head, num_layers=num_layers)
    model.zero_grad()
    model.train() # 继承的nn.Module,在训练模型时候，需要调.train()，让子模块全部转到训练状态
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    num_epoches = 6
    for t in range(0, num_epoches):
        print("current epoch is", t)
        # You can use batching if you'd like
        loss_function = nn.NLLLoss() # cross extropy for longtensor type
        count = 0
        data_chunks = text_chunking_indexed(train_text, chunk_size, vocab_index, need_whitespace=True)
        label_chunks = text_chunking_indexed(train_text, chunk_size, vocab_index, need_whitespace=False)

        chunk_idxs = [i for i in range(0, len(data_chunks))]
        random.seed(t)
        random.shuffle(chunk_idxs) # 打乱坐标来训练

        for ex_idx in chunk_idxs:
            data = data_chunks[ex_idx]
            label = label_chunks[ex_idx]
            # current_indexed_context = [26  8 13  3 20 18 19 17  8  0 11 26 22 14 17 10  4 17 18 26]
            log_probs = model(data) # 继承了nn.Module时，直接调用model(input)就可以直接得到模型输出！！！
            log_probs = torch.Tensor(log_probs).squeeze()
            
            expect_tensor = torch.Tensor(label).long()
            
            loss = loss_function(log_probs, expect_tensor)
            loss_val = loss.detach().cpu().numpy()   

            model.zero_grad()
            loss.backward()
            optimizer.step()

            count = count + 1
            if count % 200 == 0:
                print(loss_val)
        model.eval()
        print("Current spoch is ", t)
        print_evaluation(dev_text, \
                    NeuralLanguageModel(model, vocab_index, chunk_size), vocab_index, args.output_bundle_path)
        model.train()
                
    model.eval()
    return NeuralLanguageModel(model, vocab_index, chunk_size)

# final run before submission
""" 
{
  "sane": true,
  "normalizes": true,
  "range": true,
  "log_prob": -909.2762309238315,
  "avg_log_prob": -1.818552461847663,
  "perplexity": 6.162930912340994
}
Entire time of training and evaluating is  592.007673740387
""" 
            
            