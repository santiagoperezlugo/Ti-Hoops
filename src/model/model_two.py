import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

class NBA_Score_Predictor_Model(nn.Module): 
    def __init__(self, in_features): 
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )
    
    def forward(self, x):
        scores = self.layers(x)
        return scores
