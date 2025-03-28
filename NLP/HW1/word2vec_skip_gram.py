import numpy as np
import random
from collections import defaultdict
from nltk.tokenize import word_tokenize
import nltk

# 下载 punkt 分词工具
nltk.download('punkt')

# 示例文本数据
text_data = """
Natural language processing (NLP) is a field of artificial intelligence that deals with the interaction 
between computers and humans using natural language. The ultimate goal of NLP is to enable computers 
to understand, interpret, and generate human language in a way that is valuable.
Word2Vec is a technique in NLP used to compute vector representations of words. These representations
capture semantic meaning of words and are widely used for various NLP tasks such as word similarity, 
text classification, and machine translation.
"""

# 对文本进行分词
sentences = nltk.sent_tokenize(text_data)
tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]

# 构建词汇表
vocab = set(word for sentence in tokenized_sentences for word in sentence)
vocab_size = len(vocab)

# 为每个词分配一个唯一的整数ID
# --- 字符表构建各自对应的ID列表 --- #
word2index = {word: i for i, word in enumerate(vocab)}
index2word = {i: word for word, i in word2index.items()}
tokenized_vocab = [word2index[item] for item in vocab]

# word2vec用skip-gram时的训练参数
embedding_dim = 10  # 词向量维度
learning_rate = 0.05  # 学习率
decay = 0.99
epochs = 300  # 训练轮次

# 初始化每个词的上下文列表
window_size = 2  # 上下文窗口大小
full_context_list = []
# [[context_idx_1, context_idx_2, context_idx_3, context_idx_4], ..., ...]


# --- 构建原句的下标sentence_tokneized_index --- #
# --- 构建上下文字典列表，context_dict --- #

sentence_tokneized_index = list() # --- 按照顺序的tokenized sentence --- #
for sentence in tokenized_sentences:
    for i, word in enumerate(sentence): # 中心词
        central_idx = word2index[word]
        sentence_tokneized_index.append(central_idx)
        context_list = list() # --- 当前central_index的上下文列表 --- #

        for j in range(i - window_size, i + window_size + 1): # 选定左，右各window大小的上下文
            if j >= 0 and j < len(sentence) and i != j:
                context_word = sentence[j]
                context_idx = word2index[context_word]
                context_list.append(context_idx)

        full_context_list.append(context_list)


# 初始化词向量
# ------ 公式：中心词，vi和vj的初始化 ----- 
V = np.random.randn(vocab_size, embedding_dim)  # 词向量矩阵【对每个词一下子做了初始化】

# ------ 公式：上下文，ui和uj的初始化 -----
U = np.random.randn(vocab_size, embedding_dim)  # 上下文词向量矩阵【对每个词一下子做了初始化】


# 概率计算p(wo|wc)
def probability(context_index, central_index):
    numerator = np.exp(np.dot(U[context_index], V[central_index]))
    denominator = 0
    for all_context_index in tokenized_vocab:
        denominator += np.exp(np.dot(U[all_context_index], V[central_index]))
    return numerator / denominator

# 损失函数
def total_loss_fn(central_index, context_index):
    return -1 * np.log(probability(context_index, central_index))
     

# 梯度函数
def central_gradient_fn(central_index, context_index):
    sum = 0
    for all_context_index in tokenized_vocab:
        sum += probability(all_context_index, central_index) * U[all_context_index]
    return -1 * (U[context_index] - sum)

def context_central_gradient_fn(central_index, context_index):
    cal = V[central_index]*(1- probability(context_index, central_index))
    return -1 * (cal)    


# 此时是正确的
def context_not_central_gradient_fn(central_index, context_index, not_context_index):
    cal = probability(not_context_index, central_index) * V[central_index]
    return (cal)


for epoch in range(epochs):

    total_loss = 0
    if learning_rate > 0.01:
        learning_rate *= decay

    for cur_index in range(0, len(sentence_tokneized_index)): # 中心词下标 
        central_index = sentence_tokneized_index[cur_index]
        cur_context_list = full_context_list[cur_index]
        for context_index in cur_context_list: # 找到中心词的（某一个）上下文的下标
            
            # 加入损失 (负对数)
            total_loss += total_loss_fn(central_index, context_index)

            # --- 更新 1：中心词vc更新 --- #
            gradient_central = central_gradient_fn(central_index, context_index)
            V[central_index] -= learning_rate * gradient_central
            
            # --- 更新 2：对所有的背景词uo更新 --- #
            # TODO: 遍历词汇表 & 用cotext_dict识别是不是当前vc的上下文，用不同的梯度更新
            for all_context_index in tokenized_vocab:

                if all_context_index == central_index:
                    continue
                
                # --- 是当前中心词的上下文 --- #
                if all_context_index == context_index: 
                    gradient_context = context_central_gradient_fn(central_index, all_context_index)
                    U[all_context_index] -= learning_rate * gradient_context

                # --- 不是当前中心词的上下文 --- #
                else: 
                    gradient_not_context = context_not_central_gradient_fn(
                                                central_index, 
                                                context_index,
                                                all_context_index)
                    U[all_context_index] -= learning_rate * gradient_not_context
            
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss}")

# 预测词向量
def predict_word(word):
    word_idx = word2index[word]
    return V[word_idx]

# 使用训练好的模型进行预测
print("\nWord vector for 'language':", predict_word('language'))