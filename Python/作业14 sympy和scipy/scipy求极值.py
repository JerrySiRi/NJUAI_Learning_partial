'''
4. 求出函数 f(x,y,z) = x**2 + 3*x + 2*y**2 + 2*y + 3*z**2 - 4*z + 5 的极小值
并输出结果和取到最小值的x,y,z的值，手算结果验证输出的正确性。
目标：熟悉scipy的 求极值 操作。

'''
'''
最小化函数
函数表示一条曲线，曲线有高点和低点。
高点称为最大值。
低点称为最小值。
整条曲线中的最高点称为全局最大值，其余部分称为局部最大值。
整条曲线的最低点称为全局最小值，其余的称为局部最小值。
可以使用 scipy.optimize.minimize() 函数来最小化函数。

minimize() 函接受以下几个参数：
fun - 要优化的函数
x0 - 初始猜测值
method - 要使用的方法名称，值可以是：'CG'，'BFGS'，'Newton-CG'，'L-BFGS-B'，'TNC'，'COBYLA'，，'SLSQP'。
callback - 每次优化迭代后调用的函数。
options - 定义其他参数的字典：
'''
import scipy
import numpy as np
from scipy import *
from scipy.optimize import minimize
a=np.array((1,1,1))
def f(x):
    return x[0]**2 + 3*x[0] + 2*x[1]**2 + 2*x[1] + 3*x[2]**2 - 4*x[2] + 5
print(minimize(f,a))