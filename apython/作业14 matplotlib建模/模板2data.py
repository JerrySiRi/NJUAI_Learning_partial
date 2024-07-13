from cmath import nan
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data=pd.read_excel("data.xlsx")
def d(x,y):
    return (x-y)**2
myd=np.vectorize(d)

def pre(n):
    global data
    y=list(data.loc[n-1][2::])
    l=[]
    for i in range(0,245):
        y0=list(data.loc[i][2::])
        l.append(myd(y,y0).sum())
    l[n-1]=float("inf")
    p_index=l.index(min(l))
    p=list(data.loc[p_index])[1]
    while p!=p:
        l[p_index]=float("inf")
        p_index=l.index(min(l))
        p=list(data.loc[p_index])[1]
    print(p)

x=int(input())
pre(x)