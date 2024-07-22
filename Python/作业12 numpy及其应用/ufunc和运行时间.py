'''
给定一个numpy类型的3维矩阵A,请编写程序完成以下功能：
1）利用numpy的ufunc将A的第1（0,1,2维）维求积。
2）利用for循环实现上述功能，并且输出两者花费的时间。
#输入：
A=[[[0. 1.]
  [0. 1.]
  [1. 0.]]

 [[0. 1.]
  [1. 1.]
  [1. 0.]]]
#输出：
[[0. 0.]
 [0. 0.]]

'''
import numpy as np
a=[[[0., 1.],[0. ,1.],[1., 0.]],[[0., 1.],[1. ,1.],[1., 0.]]]#2*3*2
arr=np.array(a)
for i in range(0,3):
    print(np.multiply.reduce(arr,axis=i))



for i in range(0,2):#计算axis1的乘积
    for k in range(0,2):
        mul=1
        for j in range(0,3):
            mul*=arr[i,j,k]
        #print(mul)


'''
14.3 µs ± 5.19 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
1.26 ms ± 269 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
'''






