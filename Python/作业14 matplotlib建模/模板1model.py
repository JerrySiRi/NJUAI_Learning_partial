import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

near_infrared = pd.read_excel(io="作业附件.xlsx", sheet_name=0)
plt.figure(figsize=(10, 5), dpi=100)
for j in [1, 2, 3, 5, 6]:
    x = list(near_infrared.columns)
    x.remove('No')
    x.remove('OP')
    y = [near_infrared[i][j-1] for i in x]#Dataframe中的值可以通过下标来完成访问！
    plt.plot(x, y, label='No.{0}'.format(j))
plt.xlabel('wave number(/cm)')
plt.ylabel('absorbance(AU)')
plt.legend(loc='best')
plt.show()

'''
legend 函数 , 传入若干个字符串可变参数 , 系统会按照顺序为若干图形进行标识 ;

如上面的示例中 , 给第一个图形标识 sin(x) , 给第二个图形标识 cos(x) ;
常见的放置位置有: 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 
'center right', 'lower center', 'upper center', 'center' 等。

这些放置位置会对plot时候的label的放置位置产生影响
'''


near_infrared = pd.read_excel(io="作业附件.xlsx", sheet_name=0,
                              skiprows=[1, 2, 3, 4, 6, 7, 8, 10, 12, 14, 27, 32, 61, 66, 70]).groupby("OP").mean()
mid_infrared = pd.read_excel(io="作业附件.xlsx", sheet_name=1,
                             skiprows=[1, 2, 3, 4, 6, 7, 8, 10, 12, 14, 27, 32, 61, 66, 70]).groupby("OP").mean()
#拿OP中产地的名称来分类，跳过了位置产地的数据（关键字参数shiprows）
infrared = pd.merge(mid_infrared, near_infrared)#把近红外和中红外的结合在一起了（跳过了未知数据的），按照index-产地信息合成了一个
infrared_arr = np.delete(np.array(infrared.values), 0, axis=1)  # 17行，每行为数据库样本吸收率的均值。（只有对应的波长和吸收率，没有产地信息，但是知道是从1-17排列的）
'''
把这个dataframe变成了numpy，并且在axis=1这个维度删除了第一个元素（下标为0,），即这个ndarray的第一列的数据（即OP-产地信息）
'''
df1 = pd.read_excel(io="作业附件.xlsx", sheet_name=0)
df2 = pd.read_excel(io="作业附件.xlsx", sheet_name=1)
df = pd.merge(df2, df1)#按照index进行合并

for k in [5, 9, 15, 18, 25, 30, 42, 60, 68, 84, 91, 115, 126, 138, 157, 176, 185, 197, 206, 220]:
    # 65%准确率，上面这行数据是为了测量准确度的！（通过已有的数据随机选择来测量）
    # 待检测样本的检测结果分别为 14, 13, 17, 16, 5, 14, 12, 16, 4, 9, 10, 10, 13, 10, 10
    arr = np.delete(np.array(df[k-1: k].values), 0)
    arr = np.delete(arr, 0)  # 1行，为待检测样本的吸收率。
    residual = np.vectorize(lambda x, y: (x - y) ** 2)#平方差
    residual_arr = np.sum(residual(infrared_arr, arr), axis=1)
    min_residual = np.min(residual_arr)
    for i in range(17):
        if residual_arr[i] == min_residual:
            print(i + 1)
            break
