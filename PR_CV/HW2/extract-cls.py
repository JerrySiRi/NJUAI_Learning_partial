#%%
"""READEME.md， 问题简答
1. 
block 1：完成train和test的划分，并以我的学号（211300024）作为random seed从每个类中拿到一个样本
block 2：完成模型的加载（从huggingface上下载模型到本地啦，连接vpn好像也没法直接从huggingface的url下载呢（端口超时））
        并对数据集S进行前向传播，计算ViT-Tiny模型的CLS Token（默认维度为192）

2. 
block 3：完成PCA，和保存90%方差的降维
结果：
原始（未降维）的特征矩阵：torch.Size([200, 192])
原始维度: 192
PCA 后维度: 71
保留的维度比: 0.3697916666666667
"""


""" structure.txt, 项目结构（此时只上传了.py文件）
CUB_200_2011
   attributes
   dataset
      test
      train
      train_200
   images
   parts
model
   model.safetensors
   pytorch_model.bin
   config.json
extract-cls.py
"""

#%%
""" Block 1: divide data into training data and testing data
TODO: 从网页https://huggingface.co/datasets/student/CUB_birds_200_2011 
下载CUB 数据集。
1. 读取images.txt文件,获得每个图像的标签 
2. 读取train_test_split.txt文件,获取每个图像的train, test标签.其中1为训练,0为测试. 
3. 在CUB 数据集的200 个类中，从每个类的【训练集】中随机抽取1张图片，组成我们将要使用的数据集S。
在准备数据集S 时，使用你的【学号做为随机数】，从每个类中随机抽取1 张图像
"""
import os 
import shutil 
import numpy as np 
import time
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
path = current_dir + '/CUB_200_2011/'


# 文件路径
path_images = path + 'images.txt' 
path_split = path + 'train_test_split.txt' 
# 划分后的路径
train_save_path = path + 'dataset/train/' 
test_save_path = path + 'dataset/test/'
shuttle_200_train_save_path = path + 'dataset/train_200/' 

# 读取images.txt文件 ----- 不同类别中，每个image文件的名字 (类别名 + 文件名)
images = [] 
category_name = set() # 全部类别的名字

with open(path_images,'r') as f: 
    for line in f: 
        path_name = list(line.strip('\n').split(','))
        # cur_category_name =line.split(" ")[1].split("/")[0].split(".")[1]
        images.append(path_name)
        # category_name.add(cur_category_name)
        # print(path_name)


# 读取train_test_split.txt文件 --- 是训练集（1），还是测试集（0）
train_or_test_split = [] 
with open(path_split, 'r') as f_: 
    for line in f_: 
        train_or_test_split.append(list(line.strip('\n').split(',')))


# 做train和test的划分啦
num = len(images) # 图像的总个数 
for k in range(num): 
    file_name = images[k][0].split(' ')[1].split('/')[0] 
    
    # --- 训练集（1） --- 
    if int(train_or_test_split[k][0][-1]) == 1: 
        # 判断之前是否有这个类了
        if os.path.isdir(train_save_path + file_name): 
            # --- 复制操作，shutil.copy(src, dst)，把src（文件）直接复制 + 移动到dst这个位置 --- 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], train_save_path + file_name + '/' + images[k][0].split(' ')[1].split('/')[1]) 
        else: 
            os.makedirs(train_save_path + file_name) 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], train_save_path + file_name + '/' + images[k][0].split(' ')[1].split('/')[1]) 
        print('%s处理完毕!' % images[k][0].split(' ')[1].split('/')[1]) 
    
    # --- 测试集（0） --- 
    else: 
       # 判断之前是否有这个类了
        if os.path.isdir(test_save_path + file_name): 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], test_save_path+file_name+'/'+images[k][0].split(' ')[1].split('/')[1]) 
        else: 
            os.makedirs(test_save_path + file_name) 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], test_save_path + file_name + '/' + images[k][0].split(' ')[1].split('/')[1]) 
            print('%s处理完毕!' % images[k][0].split(' ')[1].split('/')[1])


# 从划分好的train中每个类别（每个文件夹）随机抽取一张图片
def copy_random_file_from_subfolders(source_dir, target_dir, seed=211300024):
    random.seed(seed)
    os.makedirs(target_dir, exist_ok=True)
    # 遍历“当前”（train_save_path）的所有子文件夹 -- 子类
    for subfolder_name in os.listdir(source_dir):
        subfolder_path = os.path.join(source_dir, subfolder_name)
        if os.path.isdir(subfolder_path):
            files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
            if files:  # 如果文件夹非空
                selected_file = random.choice(files)
                file_path = os.path.join(subfolder_path, selected_file)
                # 拷贝文件到目标文件夹，保持原文件名
                shutil.copy(file_path, os.path.join(target_dir, selected_file))
                print(f"""类别 {subfolder_name}, 完成随机选择，并复制移动这个图片""")

source_directory = train_save_path
target_directory = shuttle_200_train_save_path
copy_random_file_from_subfolders(source_directory, target_directory, seed=211300024)


#%%

""" block 2: call the model and finish inference
TODO 0: 从网页https://huggingface.co/timm/vit_tiny_patch16_224.augreg_in21k 
下载ViT-Tiny 模型

TODO 1: 针对S 中的每一张图像，可以将其输入ViT-Tiny 模型进行前
向计算，直至计算得到最后一层的CLS token。独立写代码
获得集合S 中所有图像的CLS token，组成特征集合F。这
里“独立”的意思是不要使用网络上现有的代码，但你可以在
学习网络代码后自己重写
"""

from urllib.request import urlopen
from PIL import Image
import timm
from safetensors.torch import load_file
import torch

path = os.path.dirname(os.path.abspath(__file__)) + '\\CUB_200_2011\\'
ROOT_TRAIN = path + 'dataset/train/'
ROOT_TEST = path + 'dataset/test/'
ROOT_TRAIN_200 = path + 'dataset/train_200/'
BATCH_SIZE = 16 


# 创建模型结构（num_classes=0 表示去掉分类头）
model = timm.create_model('vit_tiny_patch16_224.augreg_in21k', pretrained=False, num_classes=0)

# 加载 bin 文件（pytorch_model.bin）
state_dict = torch.load("model/pytorch_model.bin", map_location="cpu")
model.load_state_dict(state_dict, strict=False)
model.eval()

# 拿到模型配置，和前向传播模块
data_config = timm.data.resolve_model_data_config(model)
transforms = timm.data.create_transform(**data_config, is_training=False)

# 【Tip】 能用os表述路径，就不要用+/-呢！这样系统会自动判断/或者\\
output_tensor = list()
for f in os.listdir(ROOT_TRAIN_200):
    img = Image.open(os.path.join(ROOT_TRAIN_200, f))
    output = model(transforms(img).unsqueeze(0))  # output is (batch_size, num_features) shaped tensor
    # or equivalently (without needing to set num_classes=0)
    output = model.forward_features(transforms(img).unsqueeze(0))
    # output is unpooled, a (1, 197, 192) shaped tensor
    output = model.forward_head(output, pre_logits=True)
    # output is a (1, num_features) shaped tensor
    output_tensor.append(output, )

F = output_tensor


# %%
""" block 3: PCA
TODO: 集合F 应该包括200 个向量，每个向量为d 维（ViT 模型的
基础维数）。对其做PCA 运算，当保存90% 方差时，保留下
来的维度有多少个？相比d，占据了多少百分比？
"""

from sklearn.decomposition import PCA
import numpy as np

# flatten拉平操作，原来里边每个向量是(192, 1)
# 原因：sklearn.decomposition.PCA 只能处理二维输入： (样本数, 每个样本的特征维度)
tensor_F = torch.stack([torch.tensor(f).float().flatten() for f in F])
print(tensor_F.shape)  # 应该是 (200, d)

F_np = tensor_F.numpy()
# F = np.ndarray(F)  # sklearn需要ndarray
pca = PCA(n_components = 0.9)

# 拟合并转换数据
F_pca = pca.fit_transform(F_np)


print(f"原始维度: {F_np[1].shape[0]}")
print(f"PCA 后维度: {F_pca[1].shape[0]}")
ratio = F_pca[1].shape[0]/F_np[1].shape[0]
print(f"保留的维度比: {ratio}")

