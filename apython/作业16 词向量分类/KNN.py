'''
选题二：词向量分类
题目描述：
词向量（Word embedding）是自然语言处理（NLP）中十分常用的一种词语表示的方法，即将每个词语都映射为一个稠密的低维向量，其维度一般为几十或几百。

有一些研究工作提出了词向量的预训练方法，即根据大量无标注的自然语言文本训练得到其中每个词语的词向量

使其能够较好的表达出每个词语的含义（例如相似词语的词向量也较为相近），并最终为下游任务提供较好的初始化参数。

现在给定一个小规模的词向量文件，其中每行都包含了1个英文单词的类别和它所对应的50维的词向量（类别与数字都以空格隔开），一共有2类（country，sports）40个单词的词向量。

期望构建一个【基于50维词向量】进行【单词类别预测】的模型。





需要回答/解决下述问题，数据见附件word_embedding.txt：
1、说明单词类别预测是一个回归任务还是分类任务，请说明理由。

2、构建模型，使用【全部的50维特征对单词类别进行预测。】
每类前16条数据作为训练集，剩下数据作为测试集
最后需要给出模型在测试集上预测的效果（自己选择评估指标并说明原因）。

3、选择合适的降维方法，将特征【降维到适当的维度】，然后构建模型，使用降维后的特征对单词类别进行预测。
前16条数据作为训练集，剩下数据作为测试集，最后需要给出模型在测试集上预测的效果（自己选择评估标准并说明原因）。

4、思考该问题中能否使用KNN，如果不能，请说明原因；如果可以请说明如何使用。
'''
import pandas as pd
import numpy as np
import sklearn.decomposition as sk
df1=pd.read_csv("word_embedding.txt",sep='\s+',header=None)
#Q:查\s+的用处？？？

#country类的训练集np_country
df_country=df1[:][0:15]
np_c=np.array(df_country)
np_country=np.delete(np_c,0,axis=1)
#sports类的训练集np_sports
df_sports=df1[:][20:45]
np_s=np.array(df_sports)
np_sports=np.delete(np_s,0,axis=1)
#训练集np_training
np_training=np.concatenate([np_country,np_sports],axis=0)

#两者的测试集np_exam
df_exam_1=df1[:][16:20]
df_exam_2=df1[:][36:40]
np_e1=np.array(df_exam_1)
np_e11=np.delete(np_e1,0,axis=1)
np_e2=np.array(df_exam_2)
np_e22=np.delete(np_e2,0,axis=1)
np_exam=np.concatenate([np_e11,np_e22],axis=0)


#选取k=5,即看和测试集之中的点最近的7个点分别来自哪个里边，哪个多就归到哪一类之中
#本情况中没有特殊给定高维度（50）时候的相关性系数，默认就为1啦！

for i in range(0,8):#测试集的0号-7号数据
    dict1 = dict()
    for j in range(0,32):#训练集的0号-31号数据
        sum=0
        for k in range(0,50):#50维数据
            sum+=(np_exam[i][k]-np_training[j][k])**2
        dict1[j]=sum
    a=list(dict1.items())
    b=sorted(a, key=lambda x: x[1])#采用元组第二个元素的大小进行排序！！！！！lambda表达式非常好用，不用来写一个新函数传递给key了。简单函数直接用lambda表示！
    target=b[0:5]#选取7个最小的数据，看看他们分别来自哪
    for i in target:
        origin1=0
        origin2=0
        if i[0]<=15:
            origin1+=1
        if i[0]>=16:
            origin2+=1
    if origin1>origin2:
        print('country')
    else:
        print('sports')

print('\n')

#使用sklearn库进行训练库PCA降维，降到2维
np_training = np_training.T
pca = sk.PCA(n_components=2)
pca.fit(np_training)
new = pca.transform(np_training)

print(new)
for i in range(0,8):#测试集的0号-7号数据
    dict1 = dict()
    for j in range(0,32):#训练集的0号-31号数据
        sum=0
        for k in range(0,2):#2维数据
            sum+=(np_exam[i][k]-new[j][k])**2
        dict1[j]=sum
    a=list(dict1.items())
    b=sorted(a, key=lambda x: x[1])#采用元组第二个元素的大小进行排序！！！！！lambda表达式非常好用，不用来写一个新函数传递给key了。简单函数直接用lambda表示！
    target=b[0:9]#选取9个最小的数据，看看他们分别来自哪
    for i in target:
        origin1=0
        origin2=0
        if i[0]<=15:
            origin1+=1
        if i[0]>=16:
            origin2+=1
    if origin1>origin2:
        print('country')
    else:
        print('sports')











