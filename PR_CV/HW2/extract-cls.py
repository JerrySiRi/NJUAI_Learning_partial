"""
TODO 3:在CUB 数据集的200 个类中，从每个类的训练集中随机抽取1张图片，组成我们将要使用的数据集S。
在准备数据集S 时，使用你的学号做为随机数，从每个类中随机抽取1 张图像
"""


#%%
""" Block 1: divide data into training data and testing data
TODO: 从网页https://huggingface.co/datasets/student/CUB_birds_200_2011 
下载CUB 数据集。
1. 读取images.txt文件,获得每个图像的标签 
2. 读取train_test_split.txt文件,获取每个图像的train, test标签.其中1为训练,0为测试. 
"""
import os 
import shutil 
import numpy as np 
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
path = current_dir + '\\CUB_200_2011\\'
time_start = time.time()

# 文件路径
path_images = path + 'images.txt' 
path_split = path + 'train_test_split.txt' 
# 划分后的路径
train_save_path = path + 'dataset/train/' 
test_save_path = path + 'dataset/test/'

# 读取images.txt文件 ----- 不同类别中，每个image文件的名字
images = [] 
with open(path_images,'r') as f: 
    for line in f: 
        images.append(list(line.strip('\n').split(',')))

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
        # 判断之前是否已经划分过测试、训练集合 
        if os.path.isdir(train_save_path + file_name): 
            # --- 复制操作，shutil.copy(src, dst)，把src（文件）直接移动到dst这个位置 --- 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], train_save_path + file_name + '/' + images[k][0].split(' ')[1].split('/')[1]) 
        else: 
            os.makedirs(train_save_path + file_name) 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], train_save_path + file_name + '/' + images[k][0].split(' ')[1].split('/')[1]) 
        print('%s处理完毕!' % images[k][0].split(' ')[1].split('/')[1]) 
    
    # --- 测试集（0） --- 
    else: 
        # 判断之前是否已经划分过测试、训练集合
        if os.path.isdir(test_save_path + file_name): 
            aaaa = path + 'images/' + images[k][0].split(' ')[1] 
            bbbb = test_save_path+file_name+'/'+images[k][0].split(' ')[1] 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], test_save_path+file_name+'/'+images[k][0].split(' ')[1].split('/')[1]) 
        else: 
            os.makedirs(test_save_path + file_name) 
            shutil.copy(path + 'images/' + images[k][0].split(' ')[1], test_save_path + file_name + '/' + images[k][0].split(' ')[1].split('/')[1]) 
            print('%s处理完毕!' % images[k][0].split(' ')[1].split('/')[1])

time_end = time.time() 
print('CUB200训练集和测试集划分完毕, 耗时%s!!' % (time_end - time_start)) 

#%%
"""Block 2: create dataloader instances
利用Pytorch方式读取数据, 用于已下载数据集的转换,便于pytorch的读取 
"""

ROOT_TRAIN = path + 'dataset/train/'
ROOT_TEST = path + 'dataset/test/'
BATCH_SIZE = 16 

import torch 
import torchvision 
from torchvision import datasets, transforms

data_transform = transforms.Compose([ transforms.Resize(224), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) ])

def train_data_load(): # 训练集 
    root_train = ROOT_TRAIN 
    train_dataset = torchvision.datasets.ImageFolder(root_train, transform=data_transform) 
    CLASS = train_dataset.class_to_idx 
    print('训练数据label与文件名的关系:', CLASS) 
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True) 
    return CLASS, train_loader

def test_data_load(): # 测试集 
    root_test = ROOT_TEST 
    test_dataset = torchvision.datasets.ImageFolder(root_test, transform=data_transform)
    CLASS = test_dataset.class_to_idx
    print('测试数据label与文件名的关系：',CLASS)
    test_loader = torch.utils.data.DataLoader(test_dataset,
                                            batch_size=BATCH_SIZE,
                                            shuffle=True)
    return CLASS, test_loader

if __name__ == "__main__": 
    Class_train, train_loader = train_data_load() 
    Class_test, test_loader = test_data_load()


#%%

""" block 3: call the model and finish inference
TODO: 从网页https://huggingface.co/timm/vit_tiny_patch16_224.augreg_in21k 
下载ViT-Tiny 模型
"""

from urllib.request import urlopen
from PIL import Image
import timm

img = None

# BUG 发生报错，图片大小不统一诶！
for batch in train_loader:
    data, label = batch  # 通常返回一个 tuple
    print(data.shape)    # 比如 torch.Size([32, 3, 224, 224])
    print(label.shape)   # 比如 torch.Size([32])
    img = data

model = timm.create_model(
    'vit_tiny_patch16_224.augreg_in21k',
    pretrained=True,
    num_classes=0,  # remove classifier nn.Linear
)
model = model.eval()

# get model specific transforms (normalization, resize)
data_config = timm.data.resolve_model_data_config(model)
transforms = timm.data.create_transform(**data_config, is_training=False)

output = model(transforms(img).unsqueeze(0))  # output is (batch_size, num_features) shaped tensor

# or equivalently (without needing to set num_classes=0)

output = model.forward_features(transforms(img).unsqueeze(0))
# output is unpooled, a (1, 197, 192) shaped tensor

output = model.forward_head(output, pre_logits=True)
# output is a (1, num_features) shaped tensor

print(output)




"""
TODO 1: 针对S 中的每一张图像，可以将其输入ViT-Tiny 模型进行前
向计算，直至计算得到最后一层的CLS token。独立写代码
获得集合S 中所有图像的CLS token，组成特征集合F。这
里“独立”的意思是不要使用网络上现有的代码，但你可以在
学习网络代码后自己重写

"""

"""
TODO 2: 集合F 应该包括200 个向量，每个向量为d 维（ViT 模型的
基础维数）。对其做PCA 运算，当保存90% 方差时，保留下
来的维度有多少个？相比d，占据了多少百分比？
"""

# %%
