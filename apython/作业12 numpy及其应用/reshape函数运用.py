'''
给定两个int型list，长度分别为n,m。请编写程序完成以下功能：
1）将这两个list分别转换成1xn和1xm的numpy向量N,M。
2）计算N^TxM（N的转置矩阵乘上M，输出维度应为nxm）的结果。
'''
import numpy as np
n=int(input())
m=int(input())
a=[1]*n
b=[2]*m
N=np.array(a).reshape(1,n)
M=np.array(b).reshape(1,m)
print(N,M)
c=N.T*M
print(c,c.shape)

