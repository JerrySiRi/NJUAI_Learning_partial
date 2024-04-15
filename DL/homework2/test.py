
import torch
from torch import nn

a = torch.randn(3,2,4)
print(nn.Flatten(a))