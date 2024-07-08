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
import joblib


def prepare_tensors(model_data):

    # Generate the columns
    features_columns = [
        'total_pts_home', 'total_pts_away',
        'avg_pts_home', 'avg_pts_away',
        'std_dev_pts_home', 'std_dev_pts_away',
        'max_pts_home', 'max_pts_away',
        'min_pts_home', 'min_pts_away',

        'avg_fg_pct_home', 'avg_fg_pct_away',
        'std_dev_fg_pct_home', 'std_dev_fg_pct_away',
        
        'total_reb_home', 'total_reb_away',
        'avg_reb_home', 'avg_reb_away',
        'std_dev_reb_home', 'std_dev_reb_away',
        'max_reb_home', 'max_reb_away',
        'min_reb_home', 'min_reb_away',
        
        'total_ast_home', 'total_ast_away',
        'avg_ast_home', 'avg_ast_away',
        'std_dev_ast_home', 'std_dev_ast_away',
        'max_ast_home', 'max_ast_away',
        'min_ast_home', 'min_ast_away',
        
        'total_stl_home', 'total_stl_away',
        'avg_stl_home', 'avg_stl_away',
        'std_dev_stl_home', 'std_dev_stl_away',
        'max_stl_home', 'max_stl_away',
        'min_stl_home', 'min_stl_away',
        
        'total_blk_home', 'total_blk_away',
        'avg_blk_home', 'avg_blk_away',
        'std_dev_blk_home', 'std_dev_blk_away',
        'max_blk_home', 'max_blk_away',
        'min_blk_home', 'min_blk_away',
        
        'total_tov_home', 'total_tov_away',
        'avg_tov_home', 'avg_tov_away',
        'std_dev_tov_home', 'std_dev_tov_away',
        'max_tov_home', 'max_tov_away',
        'min_tov_home', 'min_tov_away',
        
        'total_pf_home', 'total_pf_away',
        'avg_pf_home', 'avg_pf_away',
        'std_dev_pf_home', 'std_dev_pf_away',
        'max_pf_home', 'max_pf_away',
        'min_pf_home', 'min_pf_away',
        
        'total_plus_minus_home', 'total_plus_minus_away',
        'avg_plus_minus_home', 'avg_plus_minus_away',
        'std_dev_plus_minus_home', 'std_dev_plus_minus_away',
        'max_plus_minus_home', 'max_plus_minus_away',
        'min_plus_minus_home', 'min_plus_minus_away'
]
    
    # Splitting data into features and targets
    features = model_data[features_columns]
    targets = model_data[['home_score', 'away_score']]

    # Splitting data into training and testing sets
    features_train, features_test, targets_train, targets_test = train_test_split(
        features, targets, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    features_train_scaled = scaler.fit_transform(features_train)
    joblib.dump(scaler, 'scaler2.pkl')
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
