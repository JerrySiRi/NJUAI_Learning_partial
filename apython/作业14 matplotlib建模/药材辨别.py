import pandas as pd
import matplotlib.pyplot as plt
'''

核心：
通过已知的不同药材在这些场地的一堆近红外、中红外光的分布情况
再通过已知的这几种药材在这个未知产地的近红外、中红外光的分布情况
来预测其他几种药材是在哪个产地生产的

excel表格中数据特征：
1、一共17个药材产地

'''
medicine_jin=pd.read_excel('C:\\Users\\86152\\Desktop\\大一下课程资料\\人工智能程序设计（python）\\matplotlibh和数学建模题目\\fujian.xlsx',sheet_name='近红外')
medicine_zhong=pd.read_excel('C:\\Users\\86152\\Desktop\\大一下课程资料\\人工智能程序设计（python）\\matplotlibh和数学建模题目\\fujian.xlsx',sheet_name='中红外')

#step1：应该按照17个产地的进行画图（画不同药材品种在这个产地近红外光和中红外光的表现）
#按照场地进行分类

#近
me_jin_chang=medicine_jin.groupby('OP')
#1.1先把一些填上0的数据库的近、中的图画出来
me_jin_chang_0=medicine_jin[medicine_jin['OP']==0]
print(me_jin_chang_0)
plt.figure(figsize=(15,8))
heng=[i for i in range(4004,10001)]
plt.scatter(heng,)

