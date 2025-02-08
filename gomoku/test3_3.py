import torch
import torch.nn as nn
import torch.optim as optim

# 定义数据集
data = [
    [1, 2, 3, 4, 5, 6, 7],
    [1, 2, 3, 4, 5, 8, 9],
    [1, 2, 3, 4, 5, 7, 2]
]

# 将数据转换为PyTorch张量
data_tensor = torch.tensor(data, dtype=torch.float32)

# 定义超参数
input_size = 1
hidden_size = 20
num_layers = 2
output_size = 10  # 假设数字范围是0-9
num_epochs = 5000
learning_rate = 0.001
model_path = 'lstm_model.pth'


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


model = LSTM(input_size, hidden_size, num_layers, output_size)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

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

# 保存模型
torch.save(model.state_dict(), model_path)
print(f'Model saved to {model_path}')

# 加载模型
model = LSTM(input_size, hidden_size, num_layers, output_size)
model.load_state_dict(torch.load(model_path))
model.eval()


# 测试模型
def predict_next_number(model, sequence):
    model.eval()
    with torch.no_grad():
        inputs = torch.tensor(sequence, dtype=torch.float32).unsqueeze(1).unsqueeze(0)
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        return predicted.item()


# 示例预测
#
#     [1, 2, 3, 4, 5, 6, 7],
#     [1, 2, 3, 4, 5, 8, 9],
#     [1, 2, 3, 4, 5, 7, 2]
test_sequence = [1, 2, 3, 4, 5, 6]
predicted_number = predict_next_number(model, test_sequence)
print(f'输入序列: {test_sequence}, 预测的下一个数字: {predicted_number}')
