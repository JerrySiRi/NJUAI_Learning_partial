'''
求出以下表达式对于x的微分以及积分，并手算结果验证输出的正确性。
目标：熟悉sympy的 微分 和 积分 操作。
'''
import sympy
from sympy import *
from sympy.abc import x
print(integrate(exp(x)*sin(x),x))