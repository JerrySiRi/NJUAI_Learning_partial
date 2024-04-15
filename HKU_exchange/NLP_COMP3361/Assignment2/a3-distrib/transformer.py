# transformer.py

import time
import torch
import torch.nn as nn
import numpy as np
import random
from torch import optim
import matplotlib.pyplot as plt
from typing import List
from utils import *
import math
import torch.nn.functional
import os

# Wraps an example: stores the raw input string (input), the indexed form of the string (input_indexed),
# a tensorized version of that (input_tensor), the raw outputs (output; a numpy array) and a tensorized version
# of it (output_tensor).
# Per the task definition, the outputs are 0, 1, or 2 based on whether the character occurs 0, 1, or 2 or more
# times previously in the input sequence (not counting the current occurrence).

# TODO：对输入、输出进行格式化处理（原始格式 、张量化格式、 input的embedding（indexed格式！））
# output是使用规则模型（for循环前后查找得到的正确结果）
class LetterCountingExample(object):
    def __init__(self, input: str, output: np.array, vocab_index: Indexer):
        self.input = input
        self.input_indexed = np.array([vocab_index.index_of(ci) for ci in input])
        self.input_tensor = torch.LongTensor(self.input_indexed)
        self.output = output
        self.output_tensor = torch.LongTensor(self.output)


# Should contain your overall Transformer implementation. You will want to use Transformer layer to implement
# a single layer of the Transformer; this Module will take the raw words as input and do all of the steps necessary
# to return distributions over the labels (0, 1, or 2).
class Transformer(nn.Module):
    def __init__(self, vocab_size, num_positions, d_model, d_internal, num_classes, num_layers):
        # model = Transformer(vocab_size=27, num_positions=20, 
        # d_model=100, d_internal=50, num_classes=3, num_layers=1)
        """
        :param vocab_size: vocabulary size of the embedding layer
        :param num_positions: max sequence length that will be fed to the model; should be 20
        :param d_model: see TransformerLayer
        :param d_internal: see TransformerLayer
        :param num_classes: number of classes predicted at the output layer; should be 3
        :param num_layers: number of TransformerLayers to use; can be whatever you want
        """
        super().__init__()
        # 整数索引序列 转换为对应的 词嵌入向量
        # utils.py中对train和dev数据都已经进行了处理，已经生成了原始data的indexed后的数据！
        # 此时只需要对indexed后的数据进行embedding转化就好啦！

        # section 1: embedding (convert to input scale: d_model)
        self.embedding_layer = nn.Embedding(vocab_size, d_model)
        self.final_embedding_layer = PositionalEncoding(d_model, num_positions)

        # section 2: Transformer (self-attention + feed-forward)
        # [single layer] self.Transformer_layer = TransformerLayer(d_model, d_internal)
        # [multiple layers]
        list_Transformer_layer = []
        for _ in range(0, num_layers-1):
            list_Transformer_layer.append(TransformerLayer(d_model, d_internal, True)) # no attention map
        list_Transformer_layer.append(TransformerLayer(d_model, d_internal, False)) # add attention map
        self.Transfomer_layer = nn.Sequential(*list_Transformer_layer)

        # section 3: linear + softmax
        self.output_layer = nn.Linear(d_model, num_classes)



    def forward(self, indices):
        """

        :param indices: list of input indices
        :return: A tuple of the softmax log probabilities (should be a 20x3 matrix) and a list of the attention
        maps you use in your layers (can be variable length, but each should be a 20x20 matrix)
        """
        # indices是data中已经转化成索引形式的embedding。
        # token_embdding是索引形式的embedding->实数embedding
        # section 1
        final_embedding = None
        attention_output = None
        token_embedding = self.embedding_layer(indices)
        final_embedding = self.final_embedding_layer.forward(token_embedding)

        # section 2
        # [single layer] trans_output,attention_output = self.Transformer_layer.forward(final_embedding)
        # [multiple layers]
        trans_output, attention_output = self.Transfomer_layer.forward(final_embedding)

        # section 3
       # print("---------", trans_output.size())
        #  trans_output的size([20, 100])
        linear_output = self.output_layer(trans_output)
        softmax_output = torch.nn.functional.log_softmax(linear_output, dim = -1)

        return softmax_output, attention_output


# Your implementation of the Transformer layer goes here. It should take vectors and return the same number of vectors
# of the same length, applying self-attention, the feedforward layer, etc.
class TransformerLayer(nn.Module):
    def __init__(self, d_model, d_internal,no_attention = False):
        """
        :param d_model: The dimension of the inputs and outputs of the layer (note that the inputs and outputs
        have to be the same size for the residual connection to work)
        :param d_internal: The "internal" dimension used in the self-attention computation. Your keys and queries
        should both be of this length.
        """
        super().__init__()
        # original one-head self-attention
        self.W_Q_layer = torch.nn.Linear(d_model, d_internal)
        self.W_K_layer = torch.nn.Linear(d_model, d_internal) # 此时假设Q,K,V不是方阵了！ 
        self.W_V_layer = torch.nn.Linear(d_model, d_internal)
        # 对每一行softmax（axis=1），每一行 = 一个query的权重
        self.softmax_layer = torch.nn.Softmax(dim = 1)
        self.d_internal = d_internal
        self.linear_reshape = torch.nn.Linear(d_internal, d_model)
        self.no_attention = no_attention

        # feed-forward
        self.feed_forward = nn.Sequential(torch.nn.Linear(d_model, 4*d_model),\
                torch.nn.ReLU(),torch.nn.Linear(4*d_model, d_model))

    def forward(self, input_vecs):

        # self-attention & residual
        K = self.W_K_layer(input_vecs)
        Q = self.W_Q_layer(input_vecs)
        V = self.W_V_layer(input_vecs)
        
        # torch.matmul()函数用于执行两个张量的矩阵相乘操作
        # torch.transpose(input, dim0, dim1),dim0和dim1是要交换的两个维度【任两个维度交换】
        # trick: division by sqrt(d_internal)
        Attention = self.softmax_layer(torch.matmul(Q, torch.transpose(K,0,1)) / math.sqrt(self.d_internal))
        #print("attention value size = ",Attention.size())
        # attention value size =  torch.Size([20, 20])
        # attention multiply size =  torch.Size([20, 100]
        O_1 = torch.matmul(Attention, V)
        O_residual_1 = self.linear_reshape(O_1) + input_vecs # output of self-attention & residual connection
        #print("attention multiply size = ", O_residual_1.size())

        # feed-forward & residual 
        O_2 = self.feed_forward(O_residual_1)
        O_residual_2 = O_2 + O_residual_1
        # BUG: 应该返回Attention矩阵，decode的时候解析每个token
        #       来看每个位置token和其他所有位置token之间的关系。也即attention值
        if self.no_attention == True:
            return O_residual_2
        return O_residual_2, Attention
        


# Implementation of positional encoding that you can use in your network
class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, num_positions: int=20, batched=False):
        """
        :param d_model: dimensionality of the embedding layer to your model; since the position encodings are being
        added to character encodings, these need to match (and will match the dimension of the subsequent Transformer
        layer inputs/outputs)
        :param num_positions: the number of positions that need to be encoded; the maximum sequence length this
        module will see【此时的数据长度是一致的，都是20】
        :param batched: True if you are using batching, False otherwise
        """
        super().__init__()
        # Dict size
        self.emb = nn.Embedding(num_positions, d_model)
        self.batched = batched

# 此时传入的x是实数的embedding（是整数的embedding也无所谓），此函数只用一个input_size!!!
# 最终返回position embedding + input embedding!!!
    def forward(self, x):
        """
        :param x: If using batching, should be [batch size, seq len, embedding dim]. Otherwise, [seq len, embedding dim]
        :return: a tensor of the same size with positional embeddings added in
        """
        # Second-to-last dimension will always be sequence length
        input_size = x.shape[-2]
        indices_to_embed = torch.tensor(np.asarray(range(0, input_size))).type(torch.LongTensor)
        if self.batched:
            # Use unsqueeze to form a [1, seq len, embedding dim] tensor -- broadcasting will ensure that this
            # gets added correctly across the batch
            emb_unsq = self.emb(indices_to_embed).unsqueeze(0)
            return x + emb_unsq
        else:
            return x + self.emb(indices_to_embed)


# This is a skeleton for train_classifier: you can implement this however you want
def train_classifier(args, train, dev, num = 1):
    print("current number of layers is ",num)
    model = Transformer(vocab_size=27, num_positions=20, \
        d_model=100, d_internal=50, num_classes=3, num_layers = num)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    num_epochs = 10
    for t in range(0, num_epochs):
        loss_this_epoch = 0.0
        random.seed(t)
        # You can use batching if you'd like
        valid_index = [i for i in range(0, len(train))]
        random.shuffle(valid_index)
        loss_function = nn.NLLLoss()
        for index in valid_index: # do not use batch 打乱原数据排序shuffle
            # TODO: Run forward and compute loss
            ex = train[index]
            model.zero_grad() # 清空梯度
            result, _ = model.forward(ex.input_tensor) # 前向计算结果 
            #print("result",result)
            #print("label", ex.output_tensor)
            loss = loss_function(result, ex.output_tensor) # 计算loss
            loss.backward() # 反向传播计算梯度 
            optimizer.step() # 依梯度来更新参数
            loss_this_epoch += loss.item()
    model.eval()
    return model


# final run before submission
"""
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
10000 lines read in
1000 lines read in
current number of layers is  1
INPUT 0: heir average albedo
GOLD 0: array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 1, 2, 0, 0, 2, 0, 0, 2])
PRED 0: array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 1, 2, 0, 0, 2, 0, 0, 2],
      dtype=int64)
INPUT 1: ed by rank and file
GOLD 1: array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 1, 1, 2, 0, 0, 0, 1, 2])
PRED 1: array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 1, 1, 2, 0, 0, 0, 1, 2],
      dtype=int64)
INPUT 2: s can also extend in
GOLD 2: array([0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 0, 0, 1, 1, 0, 2, 0, 2])
PRED 2: array([0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 0, 0, 1, 1, 0, 2, 0, 2],
      dtype=int64)
INPUT 3: erages between nine
GOLD 3: array([0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 2, 2, 0, 1, 1, 0, 2, 2, 2])
PRED 3: array([0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 2, 2, 0, 1, 1, 0, 2, 2, 2],
      dtype=int64)
INPUT 4:  that civilization n
GOLD 4: array([0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0, 1, 2, 2, 0, 0, 2, 1])
PRED 4: array([0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0, 1, 2, 2, 0, 0, 2, 1],
      dtype=int64)
Accuracy: 100 / 100 = 1.000000
Training accuracy (100 exs):
Accuracy: 1999 / 2000 = 0.999500
Dev accuracy (whole set):
Decoding on a large number of examples (1000); not printing or plotting
Accuracy: 19968 / 20000 = 0.998400
Duration: 476.32361674308777s
"""

####################################
# DO NOT MODIFY IN YOUR SUBMISSION #
####################################
def decode(model: Transformer, dev_examples: List[LetterCountingExample], do_print=False, do_plot_attn=False):
    """
    Decodes the given dataset, does plotting and printing of examples, and prints the final accuracy.
    :param model: your Transformer that returns log probabilities at each position in the input
    :param dev_examples: the list of LetterCountingExample
    :param do_print: True if you want to print the input/gold/predictions for the examples, false otherwise
    :param do_plot_attn: True if you want to write out plots for each example, false otherwise
    :return:
    """
    # 统计正确的预测数量 和 总预测数量
    num_correct = 0
    num_total = 0
    # 验证集样例过长，就不打印 & 不画图了
    if len(dev_examples) > 100:
        print("Decoding on a large number of examples (%i); not printing or plotting" % len(dev_examples))
        do_print = False
        do_plot_attn = False
    for i in range(0, len(dev_examples)):
        ex = dev_examples[i]
        # 获取模型的输出log概率（softmax后结果） 和 attention输出（self-attention & residual connection后）
        (log_probs, attn_maps) = model.forward(ex.input_tensor)
        predictions = np.argmax(log_probs.detach().numpy(), axis=1)
        if do_print:
            print("INPUT %i: %s" % (i, ex.input))
            print("GOLD %i: %s" % (i, repr(ex.output.astype(dtype=int))))
            print("PRED %i: %s" % (i, repr(predictions)))
        if do_plot_attn:
            attn_map = attn_maps # 没有采用batch的方案
            fig, ax = plt.subplots()
            # `imshow`函数是matplotlib库中用于绘制图像的函数
            im = ax.imshow(attn_map.detach().numpy(), cmap='hot', interpolation='nearest')
            ax.set_xticks(np.arange(len(ex.input)), labels=ex.input)
            ax.set_yticks(np.arange(len(ex.input)), labels=ex.input)
            ax.xaxis.tick_top()
            # plt.show()
            if not os.path.exists('plots'):
                os.mkdir('plots')
            plt.savefig("plots/{0}_attns_{1}.png".format(i, "without_batch"))
            
        acc = sum([predictions[i] == ex.output[i] for i in range(0, len(predictions))])
        num_correct += acc
        num_total += len(predictions)
    print("Accuracy: %i / %i = %f" % (num_correct, num_total, float(num_correct) / num_total))
