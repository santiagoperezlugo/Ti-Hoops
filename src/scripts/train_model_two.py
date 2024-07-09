import torch
from torch import nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
from data import convert_data as pd
from model import model_two as mo
from pathlib import Path

def train_model(train_data, test_data):
    input_size = 84
    model_two = mo.NBA_Score_Predictor_Model(input_size)

    optimizer = optim.Adam(model_two.parameters(), lr=0.001, weight_decay=0.01)
    criterion = nn.SmoothL1Loss()

    epochs = 70
    for epoch in range(epochs):
        train_correct_predictions = 0
        train_total_predictions = 0

        model_two.train()
        total_train_loss = 0.0
        for features, home_away_scores in train_data:
            optimizer.zero_grad()
            scores_output = model_two(features)
            loss = criterion(scores_output, home_away_scores)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()
            train_winner = scores_output[:, 0] > scores_output[:, 1]
            real_train_winner = home_away_scores[:, 0] > home_away_scores[:, 1]
            train_correct_predictions += (train_winner == real_train_winner).sum().item()
            train_total_predictions += scores_output.shape[0]
            
        # Evaluate accuracy
        test_correct_predictions = 0
        test_total_predictions = 0

        model_two.eval() 
        total_test_loss = 0.0
        total_test_samples = 0
        with torch.no_grad():
            for feat, actual_scores in test_data:
                predictions = model_two(feat)
                loss_test = criterion(predictions, actual_scores)
                total_test_loss += loss_test.item()
                total_test_samples += 1
                
                # Determine predicted and actual winners
                predicted_winners = predictions[:, 0] > predictions[:, 1]
                actual_winners = actual_scores[:, 0] > actual_scores[:, 1]
                test_correct_predictions += (predicted_winners == actual_winners).sum().item()
                test_total_predictions += predictions.shape[0]

        average_train_loss = total_train_loss / len(train_data)
        average_test_loss = total_test_loss / total_test_samples
        train_accuracy = (train_correct_predictions / train_total_predictions) * 100
        test_accuracy = (test_correct_predictions / test_total_predictions) * 100
        
        if epoch % 1 == 0:
            print(f'Epoch: {epoch}, Train Accuracy: {train_accuracy:.2f}%, Train Loss: {average_train_loss:.3f}, Test Loss: {average_test_loss:.3f}, Test Accuracy: {test_accuracy:.2f}%')

    MODEL_PATH = Path("saved_models") 
    MODEL_PATH.mkdir(parents=True, exist_ok=True)

    MODEL_NAME = "model_two.pth"
    MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME

    print(f"Saving model to: {MODEL_SAVE_PATH}")
    torch.save(model_two.state_dict(), MODEL_SAVE_PATH) 


