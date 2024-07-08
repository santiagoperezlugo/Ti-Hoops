import torch
from torch import nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('/Users/santi/Desktop/Hoops-Analytics') 
from data import convert_data as pd
from model import model_one as mo
from pathlib import Path


#PROTOTYPE MODEL ONE




# Load data
test_data, train_data = pd.finalizeTensors()


input_size = 44
model_0 = mo.NBA_Score_Predictor_Model(input_size)

optimizer = optim.Adam(model_0.parameters(), lr=0.0001)
criterion = nn.SmoothL1Loss()

epochs = 10000
for epoch in range(epochs):
    model_0.train()
    total_train_loss = 0.0
    for features, home_away_scores in train_data:
        optimizer.zero_grad()
        scores_output = model_0(features)
        loss = criterion(scores_output, home_away_scores)
        loss.backward()
        optimizer.step()
        total_train_loss += loss.item()

    model_0.eval() 
    total_test_loss = 0.0
    total_test_samples = 0
    with torch.no_grad():
        for feat, actual_scores in test_data:
            predictions = model_0(feat)
            loss_test = criterion(predictions, actual_scores)
            total_test_loss += loss_test.item()
            total_test_samples += 1

    average_train_loss = total_train_loss / len(train_data)
    average_test_loss = total_test_loss / total_test_samples
    if epoch % 100 == 0:
        print(f'Epoch: {epoch}, Average Train Loss: {average_train_loss:.4f} | Average Test Loss: {average_test_loss:.4f}')


# # 1. Create models directory 
# MODEL_PATH = Path("saved_models")
# MODEL_PATH.mkdir(parents=True, exist_ok=True)

# # 2. Create model save path 
# MODEL_NAME = "model_one.pth"
# MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME

# # 3. Save the model state dict 
# print(f"Saving model to: {MODEL_SAVE_PATH}")
# torch.save(model_0.state_dict(), MODEL_SAVE_PATH) 


