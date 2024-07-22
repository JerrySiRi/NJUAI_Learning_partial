import numpy as np
a=[[2,1,0,2,3],[9,5,4,2,0],[2,3,4,5,6],[1,2,3,1,0],[0,4,4,2,8]]
arr1=np.array(a)
for i in range(0,3):
    for j in range(0,3):
        print(arr1[i:i+3][j:j+3])
