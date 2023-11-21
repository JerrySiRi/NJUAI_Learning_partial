
import torch
from torch import nn

net = nn.Sequential( # 128个图像，每个图像1个channel
    nn.Conv2d(1, 32, kernel_size=8, padding=0), nn.ReLU(), # 10个filer，新的channel是10维
    nn.MaxPool2d(kernel_size=2, stride=2,padding=0),
    nn.Conv2d(32, 10, kernel_size=5, padding=0), nn.ReLU(),
    nn.MaxPool2d(kernel_size=2, stride=2,padding=0),
    nn.Flatten(),
    # 一层FC网络，3个神经元，以ReLU()作为激励函数
)

# 以下检验网络建构正确性，给出了一个随机化样本，满足输入维度要求
X = torch.rand(size=(128,1,28,28), dtype=torch.float32)
for layer in net:
    X = layer(X)
    print(layer.__class__.__name__,'output shape: \t',X.shape)