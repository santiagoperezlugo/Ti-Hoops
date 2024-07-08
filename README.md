# Hoops-Analytics

Model_one is the first model, with
        
        features_columns = [
            'total_points_home', 'total_rebounds_home', 'total_ast_home', 'total_stl_home',
            'total_blk_home', 'total_tov_home', 'total_pf_home', 'avg_points_home', 
            'avg_rebounds_home', 'avg_ast_home', 'avg_stl_home', 'avg_blk_home', 'avg_tov_home', 
            'avg_pf_home', 'max_points_home', 'max_rebounds_home', 'max_assists_home', 
            'max_steals_home', 'max_blocks_home', 'max_turnovers_home', 'max_pfs_home', 
            'min_points_home', 'min_rebounds_home', 'min_assists_home', 'min_pfs_home',
            # Repeat for away stats
            'total_points_away', 'total_rebounds_away', 'total_ast_away', 'total_stl_away',
            'total_blk_away', 'total_tov_away', 'total_pf_away', 'avg_points_away', 
            'avg_rebounds_away', 'avg_ast_away', 'avg_stl_away', 'avg_blk_away', 'avg_tov_away', 
            'avg_pf_away', 'max_points_away', 'max_rebounds_away', 'max_assists_away', 
            'max_steals_away', 'max_blocks_away', 'max_turnovers_away', 'max_pfs_away', 
            'min_points_away', 'min_rebounds_away', 'min_assists_away', 'min_pfs_away'
        ]
        and with smoothL1Loss, had 6.6 % average loss after 5000 epocs with lr of 0.0001


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
        Epoch: 4900, Average Train Loss: 1.8680 | Average Test Loss: 12.5368
        Overfitting, starting at 1000 epochs

Model_two Epoch: 9900, Average Train Loss: 7.6130 | Average Test Loss: 9.2352
        Epoch: 5000, Average Train Loss: 12.9279 | Average Test Loss: 9.9501

        128 -> 64 > 2  (44 input) Epoch: 5000, Average Train Loss: 9.4630 | Average Test Loss: 9.9281


Model_three Epoch: 1700, Average Train Loss: 8.8219 | Average Test Loss: 9.4184
                 128 -> 64 > 2  (48 input)
                 Epoch: 1600, Average Train Loss: 8.8848 | Average Test Loss: 9.3757
                 100 -> 50 > 2 (48 input)
                 Epoch: 600, Average Train Loss: 9.4015 | Average Test Loss: 9.3513
                 100, 0.5

