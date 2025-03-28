"""
当数据没有中心化时，PCA 的第一主成分（e1）会受到均值方向的影响
正确的 PCA 应该在中心化后再做 SVD
corr1 趋近 1，说明未中心化 PCA 的主方向与均值方向高度对齐
corr2 不为 1，说明中心化后的主成分不再与均值方向耦合
"""

import numpy as np
# 生成数据
np.random.seed(0)
avg = np.array([1,2,3,4,5,6,7,8,9,10])
 # 偏移量
scale_temp = [0.001, 1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001]


for scale in scale_temp:
    print("当前Scale大小为", scale)
    data = np.random.randn(5000, 10) + avg * scale # 逐元素相加，自动广播
    mean = np.mean(data, axis=0)
    normalizaed_mean = mean / np.linalg.norm(mean) # 单位化，只保留方向，而不算长度


    # 不进行归一化的特征向量 -- 降维到一维时
    _, _, Vt = np.linalg.svd(data, full_matrices=False)
    e1 = Vt[0, :]  # 注意：Python中 V 是 V^T，第一行是第一个右奇异向量


    # 进行归一化后的特征向量 -- 降维到一维时
    newdata = data - mean
    _, _, Vt_centered = np.linalg.svd(newdata, full_matrices=False)
    new_e1 = Vt_centered[0, :]
    print("特征向量", new_e1)


    # 计算方向之间的相关性
    avg_norm = avg - np.mean(avg) # 偏移量的归一化
    avg_norm /= np.linalg.norm(avg_norm) # 偏移量的单位化

    e1_norm = e1 - np.mean(e1)
    e1_norm /= np.linalg.norm(e1_norm)

    new_e1_norm = new_e1 - np.mean(new_e1)
    new_e1_norm /= np.linalg.norm(new_e1_norm)

    corr1 = (np.dot(avg_norm, e1_norm)) # avg（平均向量） 和 e1（不归一化的向量）的相关性
    print("avg vs. e1_norm", corr1)
    corr2 = (np.dot(e1_norm, new_e1_norm)) # e1 和 new_e1 的相关性
    print("e1_norm vs. new_e1_norm", corr2)

