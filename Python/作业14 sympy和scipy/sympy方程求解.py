'''

2.一元二次方程求解
①求出任意一元二次方程 a*x** 2 + b*x + c = 0 的解并输出结果（其中x为未知数，a,b,c均为常数，方程的解由a,b,c表示）。
②将a=1，b=2，c=-3带入解并输出具体的值
③自行选取一组a,b,c的值使得对应的二元一次方程没有实数解；输出结果并给出解释。
目标：熟悉sympy的 方程求解 和 变量值带入 操作。

'''

import sympy
from sympy import *
from sympy.abc import x,a,b,c
fun=Eq(a*x** 2 + b*x + c,0)
dicta={a:1,b:2,c:-3}
dictb={a:-1,b:0,c:-1}
print(solve(a*x** 2 + b*x + c,x))
print(solve((a*x** 2 + b*x + c).subs(dicta),x))
print(solve(fun.subs(dictb),x))
#默认是在复数域上的解捏