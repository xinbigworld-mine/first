#  pure transformer 随机生成的数据
import torch.nn.functional as F
import torch
from torch import nn

class TransformerClassifier(nn.Module):
    def __init__(self, input_size, output_size, num_heads, num_layers, dropout=0.1):
        super(TransformerClassifier, self).__init__()
        self.transformer_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=input_size, nhead=num_heads),
            num_layers
        )
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, x):
        x_transformer = self.transformer_encoder(x)
        x_mean = x_transformer.mean(dim=1)  # 对序列维度求平均
        output = self.fc(x_mean)
        return F.log_softmax(output, dim=-1)

# 定义模型参数
input_size = 20  # 输入向量维度，假设为 20
output_size = 2  # 输出类别数，假设为 2
batch_size = 32  # 批量大小，假设为 32
num_heads = 4  # Transformer 注意力头数
num_layers = 2  # Transformer 层数
dropout = 0.1  # dropout率

# 初始化模型
model = TransformerClassifier(input_size, output_size, num_heads, num_layers, dropout)

# 假设有一个批量大小为 32 的流量数据，每个流量序列长度为 20
# 创建随机输入数据
x = torch.randint(-1, 2, (batch_size, 20, input_size)).float()  # 假设输入数据为 1,-1 的流量序列

# 调用模型进行前向传播
output = model(x)
print("输出张量的形状：", output.shape)
