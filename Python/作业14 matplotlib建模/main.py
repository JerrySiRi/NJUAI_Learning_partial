import pandas as pd

left=pd.DataFrame({'key':['foo','bar'],'lval':[1,2]},index=[0,1])
right=pd.DataFrame({'key':['foo','bar'],'lval':[4,5]},index=[0,1])
print(left)
print(right)
a=pd.merge(left,right,on='key')
print(a)
