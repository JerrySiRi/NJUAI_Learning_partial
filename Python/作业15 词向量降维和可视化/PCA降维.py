'''
题目描述：
词向量（Word embedding）是自然语言处理（NLP）中十分常用的一种词语表示的方法，即将每个词语都映射为一个稠密的高维向量，其维度一般为几十或几百。
有一些研究工作提出了【词向量的预训练方法】，即【根据大量无标注的自然语言文本】训练【得到其中每个词语的  词向量】
【使其能够较好的表达出每个词语的含义】（例如相似词语的词向量也较为相近），并最终为下游任务提供较好的初始化参数。数据预处理！

现在给定一个小规模的词向量文件（附件中的txt文件），其中每行都包含了1个英文单词和它所对应的50维的词向量（单词与数字都以空格隔开），一共有23个单词的词向量。
需要编程实现以下功能：
1、尝试自行实现PCA降维的方法并将所有词向量都降维到2维。
2、使用sklearn库中实现的PCA降维方法将词向量降维到2维。
3、将上述两种方法降维后的向量以散点图的形式进行可视化。、


要求：
本次作业以报告的形式提交，需要提供一份实验报告和代码，将报告和代码打包成压缩文件提交。
报告需包含以下内容：
1、算法描述：手动实现PCA算法的思路，遇见的难点以及解决方法。
2、可视化：将降维后的词向量以散点图的形式可视化，并标注上每个向量对应的英文单词。（类似图1的形式）
3、实验结果：汇报使用两种算法实现的情况下，降维后的可视化结果是否符合预期，即在可视化图中相似单词的向量是否距离相近
（例如在图1中各个国家单词和各个交通工具单词之间都离得较近），以及实验结果间的差别。


'''
'''
numpy中的delete函数有三个参数：
numpy.delete(arr, obj, axis)
arr：需要处理的矩阵
obj：在什么位置处理
axis：这是一个可选参数，axis = None，1，0

axis=None：arr会先按行展开，然后按照obj，删除第obj-1（从0开始）位置的数，返回一个行矩阵。

axis = 0：arr按行删除

axis = 1：arr按列删除

所有操作都是在arr的副本进行，需要有变量接收返回值。

'''
import pandas as pd
import numpy as np
import sklearn.decomposition as sk
import matplotlib.pyplot as plt
df1=pd.read_csv("tiny_word_vectors.txt",sep=' ',header=None)
df2=df1[0:23]
np_f=np.array(df2)
np_final=np.delete(np_f,0,axis=1)
'''
原因：
输出出来的是除了china那条消息全部都有的！因为china没有作为index在dataframe中存在，而是作为了column
解决：
文件标头名是附加的自定义名称，但是您会发现，原来的标头名（列标签名）并没有被删除，此时您可以使用header 参数来删除它。
让header=None》》没有标头了！
也可以显示设置标头为names，来设置自定义的Ecolumns
'''

#实现降维
np_final=np_final.T #X
average = np.average(np_final, axis=0)
np_final -= average    #零均值化
np_xie=np.matmul(np_final, np.transpose(np_final))#协方差矩阵
#如果直接计算特征值、特征向量的话，回报错
#报错的原因：没有满足same kind的原则，乘法乘出来的数没有统一格式！即不全是float64格式的》》重新创建一个统一格式的ndarray
np_xie_final=np.array(np_xie,dtype=float)
eigvals,eigvectors=np.linalg.eigh(np_xie_final)#计算得到特征值、特征向量
eig_tar=eigvectors[0:2,:]#降到两维度
data_tar=np.array(np.matmul(eig_tar,np_final))
data_tar=data_tar.T
plt.figure(figsize=(10, 5))
x = []
y = []
txt = []
for i in range(23):
    x.append(data_tar[i][0])
    y.append(data_tar[i][1])
    txt.append(df1[0][i])
plt.scatter(x, y)
for i in range(23):
    plt.annotate(txt[i], xy=(x[i], y[i]), xytext=(x[i]+0.02, y[i]+0.02))
plt.show()



#以下使用sklearn库中函数
np_final = np_final.T
pca = sk.PCA(n_components=2)
pca.fit(np_final)
new = pca.transform(np_final)
plt.figure(figsize=(10, 5), dpi=100)
x = []
y = []
txt = []
for i in range(23):
    x.append(new[i][0])
    y.append(new[i][1])
    txt.append(df1[0][i])
plt.scatter(x, y)
for i in range(23):
    plt.annotate(txt[i], xy=(x[i], y[i]), xytext=(x[i]+0.02, y[i]+0.02))
plt.show()









