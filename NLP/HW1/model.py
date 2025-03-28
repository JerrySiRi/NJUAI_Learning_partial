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

# 为每个词分配一个唯一的整数ID（类似neural model 的tokenization的操作，用于索引X_{ij}啦~）
word2index = {word: i for i, word in enumerate(vocab)}
index2word = {i: word for word, i in word2index.items()}

# 初始化共现矩阵 & 定义共现矩阵中count的指标（上下文窗口大小）
window_size = 2  # 上下文窗口大小
co_occurrence_matrix = defaultdict(lambda: defaultdict(int)) # 【二维字典】


# 构建共现矩阵
# ------ 公式：计算X_{ij}共现矩阵 ----- 
for sentence in tokenized_sentences:

    for i, word in enumerate(sentence): # 中心词
        target_idx = word2index[word]

        for j in range(i - window_size, i + window_size + 1): # 选定左，右各window大小的上下文
            if j >= 0 and j < len(sentence) and i != j:
                context_word = sentence[j]
                context_idx = word2index[context_word]
                co_occurrence_matrix[target_idx][context_idx] += 1


# GloVe的训练参数
embedding_dim = 10  # 词向量维度
learning_rate = 0.05  # 学习率
epochs = 100  # 训练轮次
alpha = 0.75  # 加权函数的指数
x_max = 100  # 加权函数的阈值


# 初始化词向量
# ------ 公式：中心词，vi和vj的初始化 ----- 
W = np.random.randn(vocab_size, embedding_dim)  # 词向量矩阵【对每个词一下子做了初始化】

W_prime = np.random.randn(vocab_size, embedding_dim)  # 上下文词向量矩阵
# ------ 公式：上下文，vi和vj的初始化 -----

b = np.zeros(vocab_size)  # 词偏置
# ------ 公式：中心词，bi和bj（每个词的偏置不一样呢~） ------

b_prime = np.zeros(vocab_size)  # 上下文词偏置
# ------ 公式：上下文，bi和bj（每个词的偏置不一样呢~） ------


# 加权函数，公式中的f
def weighted_loss(x):
    if x < x_max:
        return (x / x_max) ** alpha
    else:
        return 1
    
# 损失函数
def loss_fn(i, j, co_occurrence):
    weight = weighted_loss(co_occurrence)
    dot_product = np.dot(W[i], W_prime[j]) + b[i] + b_prime[j]
    return weight * (dot_product - np.log(co_occurrence)) ** 2


# 训练 GloVe 模型
for epoch in range(epochs):
    total_loss = 0
    for i in range(vocab_size):
        for j in co_occurrence_matrix[i]:
            co_occurrence = co_occurrence_matrix[i][j]
            # 计算损失函数
            loss = loss_fn(i, j, co_occurrence)
            total_loss += loss
            
            # 计算梯度
            weight = weighted_loss(co_occurrence)
            common_term = weight * (np.dot(W[i], W_prime[j]) + b[i] + b_prime[j] - np.log(co_occurrence))
            
            # 更新参数
            W[i] -= learning_rate * common_term * W_prime[j]
            W_prime[j] -= learning_rate * common_term * W[i]
            b[i] -= learning_rate * common_term
            b_prime[j] -= learning_rate * common_term
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss}")

# 预测词向量
def predict_word(word):
    word_idx = word2index[word]
    return W[word_idx]

# 使用训练好的模型进行预测
print("\nWord vector for 'language':", predict_word('language'))
