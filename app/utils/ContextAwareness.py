from torch import nn
import torch
import numpy as np
from torch.nn import TransformerEncoder, TransformerEncoderLayer

#记得自己手动加一下CLS
class ContextFormer(nn.Module):
    def __init__(self, input_size, output_size):
        super(ContextFormer, self).__init__()
        self.fc1 = nn.Linear(input_size, 512)
        self.edl = TransformerEncoderLayer(d_model=512, nhead=8)
        self.ed1 = TransformerEncoder(self.edl, num_layers=6)
        self.fc2 = nn.Linear(512, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.ed1(x)[:, 0]
        x = torch.softmax(self.fc2(x), dim=-1)
        return x




class ContextLSTM(nn.Module):
    def __init__(self, input_size, output_size):
        super(ContextLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size, hidden_size=16, num_layers=2, batch_first=True)
        self.fc1 = nn.Linear(16, output_size)
    def forward(self, x):
        x, _ = self.lstm1(x)
        x = self.fc1(x[:, -1, :])
        x = torch.softmax(x, dim=-1)
        return x
# rand_input = torch.rand(size=(64, 90, 13))
# model = ContextLSTM(13, 6)
