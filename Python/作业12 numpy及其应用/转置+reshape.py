'''
给定一个列表以及两个整数 N 和 M，比如列表 = [1,2,3,4,5,6]，N = 2，M = 3。
请使用程序完成以下任务：（1）将列表转换成一个N行M列的numpy矩阵 a（2）改变矩阵a的形状，将其变成一个 M x N的矩阵 b（3）对矩阵 a 进行转置操作使其变成矩阵 c。
并根据实验结果说出（2）和（3）这两个操作返回的矩阵 b 和 c 是否相同，如果不同请结合数据内在的存储表示叙述这两个操作的区别。

目标：熟悉numpy的 转置 和reshape操作。
'''
import numpy as np
N = 2
M = 3
myarray=np.array([1,2,3,4,5,6]).reshape((N,M))
print(myarray)
myarray1=np.array(myarray).reshape((M,N))#在内部实现（一位数组之中直接进行strides的改变--改变了矩阵的形状）
print(myarray1)
myarray2=myarray1.T
print(myarray2)

'''
reshape（3,2）的strides是（8,4）
T（转置）的strides---改成了列主序了！是（4,12）.在成型的二维矩阵中来看哦
'''