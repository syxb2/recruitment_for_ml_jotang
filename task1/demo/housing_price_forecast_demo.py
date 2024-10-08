import pandas

train_file_path = '../data/train.csv'
test_file_path = '../data/test.csv'
train_data = pandas.read_csv(train_file_path) # 加载 CSV 文件
test_data = pandas.read_csv(test_file_path)

# 显示数据的前几行以及基本信息
train_data_info = train_data.info()
train_data_head = train_data.head()

train_data_head

print('------------------------------------------------------------------------')

test_data_info = test_data.info()
test_data_head = test_data.head()

test_data_head

from sklearn.preprocessing import StandardScaler # 用于数据预处理

# 分离特征和目标变量
X_train = train_data.drop(columns=['ID', 'medv'])  # 训练集特征：移除ID和medv列
y_train = train_data['medv']  # 训练集目标变量：只保留medv列

X_test = test_data.drop(columns=['ID']) # 测试集特征：移除ID列

y_test_path = '../data/submission_example.csv'
y_test_data = pandas.read_csv(y_test_path)
y_test = y_test_data['medv'] # 测试集目标变量：只保留medv列

# 标准化特征
scaler = StandardScaler() # 标准化特征通过删除均值并缩放到单位方差。
X_train_scaled = scaler.fit_transform(X_train) # 将数据拟合，然后转换它。将变换器拟合到 X 和 y
X_test_scaled = scaler.transform(X_test) # 按照中心化和缩放进行标准化。

# X_train_scaled[:5]
# y_train[:5]  # 查看前5个样本的数据处理结果

import torch
import torch.nn as nn
import torch.optim as optim

# 转换数据为Tensor格式
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32) # 将数据转换为张量，dtype=torch.float32表示数据类型为32位浮点数
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1) # 将数据转换为张量，并且将数据形状转换为（n,1），即一列，n行，n为样本数。view：Returns a new tensor with the same data as the self tensor but of a different shape. 参数 -1 表示自动计算行数，1 表示列数
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

class BostonHousingModel(nn.Module):
    def __init__(self):
        super(BostonHousingModel, self).__init__()
        self.fc1 = nn.Linear(13, 64) # 输入层：输入13个特征，输出64个节点
        self.fc2 = nn.Linear(64, 32) # 隐藏层：输入64个节点，输出32个节点
        self.fc3 = nn.Linear(32, 1) # 输出层：输出一个房价预测值

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 实例化模型
model = BostonHousingModel()

loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 200
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()  # 清除之前的梯度
    predictions = model(X_train_tensor)
    loss = loss_fn(predictions, y_train_tensor)
    loss.backward()  # 反向传播
    optimizer.step()  # 更新模型参数

    # 每隔20个epoch输出一次损失
    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")
        
model.eval()
with torch.no_grad():
    test_predictions = model(X_test_tensor)
    test_loss = loss_fn(test_predictions, y_test_tensor)

print(f"Test Loss: {test_loss.item()}")
