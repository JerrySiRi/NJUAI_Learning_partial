import torch
import torch.nn as nn
import torch.nn.functional as F

# Encoder实现

condition_size = 10 #10个数字，用一个10维向量作为CVAE的条件（0-9十个数字，依label给出one-hot编码）
ignore = True # 是否需要忽略训练信息的输出

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def onehot(label): # CVAE为了要和input（1*28*28）可以concatenate，需要扩展成3维的(后续还有batch_size就变成三维)
    label = label.unsqueeze(1)
    label = label.unsqueeze(2)
    #print(label.size(0))
    exp_vec = torch.zeros(label.size(0), 1, condition_size).to(device)
    # 【新创建的，和已在cuda上tensor无关，不知道应该放在哪里！！！】
    exp_vec.scatter_(2, label, 1) # 根据label，对exp_vec进行操作，填写到维度为1的对应位置
    return exp_vec

class Encoder(nn.Module):
    def __init__(self, x_dim, hidden_size, latent_size, arch="AE", **kwargs) -> None:
        super(Encoder, self).__init__()
        self.mu = nn.Sequential(nn.Linear(x_dim, hidden_size), nn.ReLU(), nn.Linear(hidden_size, latent_size),)
        self.arch = arch
        if self.arch == "VAE":  # 若encoder返回的是均值与标准差(VAE、CVAE), 需要额外生成mu和sigma（两架构可以一样）
            self.sigma = nn.Sequential(nn.Linear(x_dim, hidden_size), nn.ReLU(), nn.Linear(hidden_size, latent_size),)

        if self.arch == "CVAE":
            self.mu = nn.Sequential(nn.Linear(x_dim + condition_size, hidden_size), nn.ReLU(), nn.Linear(hidden_size, latent_size),)
            self.sigma = nn.Sequential(nn.Linear(x_dim + condition_size, hidden_size), nn.ReLU(), nn.Linear(hidden_size, latent_size),)
        
        if self.arch == "PCA":
            self.mu = nn.Linear(x_dim,latent_size)# 根据PCA最优解，不设置偏置项


    def forward(self, xs, label=None):# 只有CVAE才会传入label，xs是输入的图片，784*1*batchsize
        # 实现编码器的forward过程，arch架构的不同取值意味着我们需要不同输出的encoder

        if self.arch == "AE":
            output = self.mu(xs) # AE的输出，只有一个code
        elif self.arch == "VAE":# VAE的输出，有mu和sigma两个输出
            mu = self.mu(xs)
            sigma = self.sigma(xs)
            output = (mu,sigma)
        elif self.arch == "CVAE": # CVAE的输出，有mu和sigma两个，但是输入还有希望生成数据的label！先扩展、再concatenate起来
            label = onehot(label)
            # print("dim_image",xs.shape)
            # print("label_image",label.shape)
            xs= torch.cat((xs, label), dim=-1)
            # xs = xs.to(device)     # Bug：不用等号赋值，就没办法移动到cuda上！
            mu = self.mu(xs)
            sigma = self.sigma(xs)
            output = (mu,sigma)
        elif self.arch == "PCA":
            output = self.mu(xs) # 线性层处理
        return output