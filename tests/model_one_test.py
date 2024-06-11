import torch
from torch import nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('/Users/santi/Desktop/Hoops-Analytics') 
from data import prepare_data as pd
from model import model_one as mo
from pathlib import Path


model_one = mo.NBA_Score_Predictor_Model()
model_one.load_state_dict(torch.load('saved_models/model_one.pth'))

model_one.eval()
