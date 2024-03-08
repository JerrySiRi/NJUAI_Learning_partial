import torch
import torch.nn as nn

# 定义输入的维度、序列长度和批量大小
input_dim = 512
seq_length = 10
batch_size = 2

# 创建一个Transformer编码器
encoder_layer = nn.TransformerEncoderLayer(d_model=input_dim, nhead=8)
transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=6)

# 创建一个随机输入张量
input_tensor = torch.randn(seq_length, batch_size, input_dim)

# 将输入张量传递给Transformer编码器
output_tensor = transformer_encoder(input_tensor)

print(output_tensor.shape)  # 输出：torch.Size([seq_length, batch_size, input_dim])