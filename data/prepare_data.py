import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler
import sys
from .load_data import getData
from sklearn.model_selection import train_test_split

import torch.optim as optim
import torch.nn as nn
import numpy as np


def prepare_tensors(model_data):
    # Define the columns that will be used as features for the model
    features_columns = [
        'total_points_home', 'total_rebounds_home', 'total_ast_home', 'total_stl_home',
        'total_blk_home', 'total_tov_home', 'total_pf_home', 'avg_points_home', 
        'avg_rebounds_home', 'avg_ast_home', 'avg_stl_home', 'avg_blk_home', 'avg_tov_home', 
        'avg_pf_home', 'max_points_home', 'max_rebounds_home', 'max_assists_home', 
        'max_steals_home', 'max_blocks_home', 'max_turnovers_home', 'max_pfs_home', 
        'min_points_home', 'min_rebounds_home', 'min_assists_home', 'min_pfs_home',
        
        'total_points_away', 'total_rebounds_away', 'total_ast_away', 'total_stl_away',
        'total_blk_away', 'total_tov_away', 'total_pf_away', 'avg_points_away', 
        'avg_rebounds_away', 'avg_ast_away', 'avg_stl_away', 'avg_blk_away', 'avg_tov_away', 
        'avg_pf_away', 'max_points_away', 'max_rebounds_away', 'max_assists_away', 
        'max_steals_away', 'max_blocks_away', 'max_turnovers_away', 'max_pfs_away', 
        'min_points_away', 'min_rebounds_away', 'min_assists_away', 'min_pfs_away'
    ]

    # Splitting the data into features and targets
    features = model_data[features_columns]
    targets = model_data[['home_score', 'away_score']]

    # Splitting the data into training and testing sets
    features_train, features_test, targets_train, targets_test = train_test_split(
        features, targets, test_size=0.2, random_state=42
    )

    # Scaling the features
    scaler = StandardScaler()
    features_train_scaled = scaler.fit_transform(features_train)
    features_test_scaled = scaler.transform(features_test)

    # Creating Tensor datasets
    train_dataset = TensorDataset(torch.tensor(features_train_scaled.astype(np.float32)),
                                  torch.tensor(targets_train.values.astype(np.float32)))
    test_dataset = TensorDataset(torch.tensor(features_test_scaled.astype(np.float32)),
                                 torch.tensor(targets_test.values.astype(np.float32)))

    # Creating DataLoaders
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    return train_dataloader, test_dataloader


def finalizeTensors():
    df_2018 = getData()
    train_data, test_data = prepare_tensors(df_2018)
    return train_data, test_data