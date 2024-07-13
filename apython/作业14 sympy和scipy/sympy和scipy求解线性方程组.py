'''

3. 请分别使用sympy和scipy求解以下的线性方程组。
   x+3*y+z = 10
2*x+y+3*z = 13
2*x+2*y+z =  9
目标：熟悉sympy和scipy的 线性方程求解 操作。

'''
#sympy之中

import sympy
from sympy import *
from sympy.abc import x,y,z
import numpy as np
import scipy
fun1=Eq(x+3*y+z,10)
fun2=Eq(2*x+y+3*z,13)
fun3=Eq(2*x+2*y+z,9)

print(solve([fun1,fun2,fun3],[x,y,z],dict=True))


'''
numpy.linalg模块的函数：
1、diag 函数 一维数组的是返回方针的对角线元素
2、dot 矩阵乘法
3、trace【trest】求迹，即对角线元素的和
4、det 求矩阵的行列式
5、eig [aige]计算方针的本征值和本征向量
6、inv 计算方针的逆
7、qr 计算qr分解
8、svd 计算奇异值的分解svd
9、solve 解决线性方程组的解Ax =b，其中A为方针
10、lstsq 计算Ax =b的最小二乘解

'''
a=[[1,3,1],[2,1,3],[2,2,1]]
b=[10,13,9]
a_=np.array(a)
b_=np.array(b)
print(np.linalg.solve(a_,b_))