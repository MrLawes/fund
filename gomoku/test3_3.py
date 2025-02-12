# torch: PyTorch库，用于构建和训练深度学习模型。
# torch.nn: 包含神经网络模块和损失函数。
# torch.optim: 包含各种优化算法。
import torch
import torch.nn as nn
import torch.optim as optim

# data: 一个包含多个序列的列表，每个序列由7个整数组成。
# data_tensor: 将data转换为PyTorch张量，并指定数据类型为float32。
# 定义数据集
data = [
    [1, 2, 3, 4, 5, 6, 7],
    [1, 2, 3, 4, 5, 8, 9],
    [1, 2, 3, 4, 5, 7, 2],
    [0, 0, 0, 0, 0, 1, 2],
]

# 将数据转换为PyTorch张量
data_tensor = torch.tensor(data, dtype=torch.float32)

# input_size: 输入特征的维度（每个时间步输入一个数字）。
# hidden_size: LSTM隐藏层的大小。
# num_layers: LSTM层数。
# output_size: 输出类别数（假设是0-9之间的数字）。
# num_epochs: 训练轮数。
# learning_rate: 学习率。
# model_path: 模型保存路径。
# 定义超参数
input_size = 1
hidden_size = 20
num_layers = 2
output_size = 15  # 假设数字范围是0-9
num_epochs = 10000
learning_rate = 0.001
model_path = 'lstm_model.pth'


# LSTM类继承自nn.Module，定义了一个LSTM模型。
# __init__方法初始化LSTM层和全连接层。
# forward方法定义了前向传播过程：
# 初始化隐状态h0和细胞状态c0。
# 使用LSTM层处理输入序列。
# 取最后一个时间步的输出并传递给全连接层，得到最终输出。
# 定义LSTM模型
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # 对于批量数据，h0和c0应该是3维的
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


# model: 创建LSTM模型实例。
# criterion: 使用交叉熵损失函数，适用于多分类任务。
# optimizer: 使用Adam优化器。
model = LSTM(input_size, hidden_size, num_layers, output_size)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 迭代训练模型：
# 准备输入和目标数据。
# 前向传播计算输出和损失。
# 反向传播更新模型参数。
# 每隔1000个epoch打印一次损失值。
# 训练模型
for epoch in range(num_epochs):
    # 准备输入和目标数据
    inputs = data_tensor[:, :-1].unsqueeze(2)  # 添加输入维度 (batch_size, sequence_length, input_size)
    targets = data_tensor[:, -1].long()  # 目标张量是最后一个元素 (batch_size)

    # 前向传播
    outputs = model(inputs)
    loss = criterion(outputs, targets)

    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 1000 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# 保存模型参数到文件。
# 加载保存的模型参数并设置为评估模式。
# 保存模型
torch.save(model.state_dict(), model_path)
print(f'Model saved to {model_path}')

# 加载模型
model = LSTM(input_size, hidden_size, num_layers, output_size)
model.load_state_dict(torch.load(model_path))
model.eval()


# predict_next_number函数用于预测给定序列的下一个数字。
# 将测试序列转换为张量并传递给模型进行预测。
# 打印预测结果。
# 测试模型
def predict_next_number(model, sequence):
    model.eval()
    with torch.no_grad():
        inputs = torch.tensor(sequence, dtype=torch.float32).unsqueeze(1).unsqueeze(0)
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        return predicted.item()


# 示例预测
print(f'{data=}')
for test_sequence in data:
    test_sequence = test_sequence[:-1]
    predicted_number = predict_next_number(model, test_sequence)
    print(f'输入序列: {test_sequence}, 预测的下一个数字: {predicted_number}')

test_sequence = [1, 2, 3, 4, 5, 8]
predicted_number = predict_next_number(model, test_sequence)
print(f'输入序列: {test_sequence}, 预测的下一个数字: {predicted_number}')

test_sequence = [0, 1, ]
predicted_number = predict_next_number(model, test_sequence)
print(f'输入序列: {test_sequence}, 预测的下一个数字: {predicted_number}')
