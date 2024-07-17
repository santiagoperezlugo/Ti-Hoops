import torch
import sys
from model import model_two as md
from main import connect_to_db
from data import load_data as ld
from sklearn.preprocessing import StandardScaler
import pandas as pd
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
import joblib
import json
import math


def find_player_stats(cursor, player_name, season, team_abbrev):
    team_abbrev = team_abbrev.upper()
    get_team_id_query = "SELECT team_id from teams WHERE team_abbreviation = %s"
    cursor.execute(get_team_id_query, (team_abbrev,))
    team_id = cursor.fetchone()
    if not team_id:
        return None, f"No data found for player {player_name} in season {season} for team {team_abbrev}"

    team_id = team_id[0]
    query = """
    SELECT 
        avg_pts, avg_fg_pct, avg_reb, avg_ast, avg_stl, avg_blk, avg_tov, avg_pf, avg_plus_minus
    FROM player_season_averages
    WHERE player_name = %s AND team_id = %s AND season = %s
    """
    cursor.execute(query, (player_name, team_id, season))
    stats = cursor.fetchone()
    if not stats:
        return None, f"No data found for player {player_name} in season {season} for team {team_abbrev}"
    return stats, None


def insert_player_stats(cursor, player_name, season, team_id, stat_tuple):
         query = """
        INSERT INTO matchup (team_id, player_name, season, avg_pts, avg_fg_pct, avg_reb, avg_ast, avg_stl, avg_blk, avg_tov, avg_pf, avg_plus_minus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
         params = (team_id, player_name, season) + stat_tuple
         cursor.execute(query, params)
         
def prepare_team_data(cursor, team_dict, team_id):
    errors = []
    for player, info in team_dict.items():
        stats, error = find_player_stats(cursor, player, info['season'], info['team'])
        if error:
            errors.append(error)
        if stats:
            insert_player_stats(cursor, player, info['season'], team_id, stats)
    return errors




def get_query(cursor):
        aggregated_stats_query = """
                SELECT
                season,
                team_id, 
                SUM(avg_pts) AS total_pts,
                AVG(avg_pts) AS avg_pts,
                STDDEV(avg_pts) AS std_dev_pts,
                MAX(avg_pts) AS max_pts,
                MIN(avg_pts) AS min_pts,

                AVG(avg_fg_pct) AS avg_fg_pct,
                STDDEV(avg_fg_pct) AS std_dev_fg_pct,

                SUM(avg_reb) AS total_reb,
                AVG(avg_reb) AS avg_reb,
                STDDEV(avg_reb) AS std_dev_reb,
                MAX(avg_reb) AS max_reb,
                MIN(avg_reb) AS min_reb,

                SUM(avg_ast) AS total_ast,
                AVG(avg_ast) AS avg_ast,
                STDDEV(avg_ast) AS std_dev_ast,
                MAX(avg_ast) AS max_ast,
                MIN(avg_ast) AS min_ast,

                SUM(avg_stl) AS total_stl,
                AVG(avg_stl) AS avg_stl,
                STDDEV(avg_stl) AS std_dev_stl,
                MAX(avg_stl) AS max_stl,
                MIN(avg_stl) AS min_stl,

                SUM(avg_blk) AS total_blk,
                AVG(avg_blk) AS avg_blk,
                STDDEV(avg_blk) AS std_dev_blk,
                MAX(avg_blk) AS max_blk,
                MIN(avg_blk) AS min_blk,

                SUM(avg_tov) AS total_tov,
                AVG(avg_tov) AS avg_tov,
                STDDEV(avg_tov) AS std_dev_tov,
                MAX(avg_tov) AS max_tov,
                MIN(avg_tov) AS min_tov,

                SUM(avg_pf) AS total_pf,
                AVG(avg_pf) AS avg_pf,
                STDDEV(avg_pf) AS std_dev_pf,
                MAX(avg_pf) AS max_pf,
                MIN(avg_pf) AS min_pf,

                SUM(avg_plus_minus) AS total_plus_minus,
                AVG(avg_plus_minus) AS avg_plus_minus,
                STDDEV(avg_plus_minus) AS std_dev_plus_minus,
                MAX(avg_plus_minus) AS max_plus_minus,
                MIN(avg_plus_minus) AS min_plus_minus
                FROM matchup
                GROUP BY team_id;
        """

        cursor.execute(aggregated_stats_query)
        all_stats_data = cursor.fetchall()
        return all_stats_data

def convert_to_dataframe(all_players_data):
    columns = ['season', 'team_id']
    columns.extend([
        'total_pts', 'avg_pts', 'std_dev_pts', 'max_pts', 'min_pts',
        'avg_fg_pct', 'std_dev_fg_pct',
        'total_reb', 'avg_reb', 'std_dev_reb', 'max_reb', 'min_reb',
        'total_ast', 'avg_ast', 'std_dev_ast', 'max_ast', 'min_ast',
        'total_stl', 'avg_stl', 'std_dev_stl', 'max_stl', 'min_stl',
        'total_blk', 'avg_blk', 'std_dev_blk', 'max_blk', 'min_blk',
        'total_tov', 'avg_tov', 'std_dev_tov', 'max_tov', 'min_tov',
        'total_pf', 'avg_pf', 'std_dev_pf', 'max_pf', 'min_pf',
        'total_plus_minus', 'avg_plus_minus', 'std_dev_plus_minus', 'max_plus_minus', 'min_plus_minus'
    ])

    df = pd.DataFrame(all_players_data, columns=columns)
    df[columns] = df[columns].fillna(0)

    home_df = df[df['team_id'] == 0].add_suffix('_home')
    away_df = df[df['team_id'] == 1].add_suffix('_away')

    home_df.reset_index(drop=True, inplace=True)
    away_df.reset_index(drop=True, inplace=True)

    merged_df = pd.concat([home_df, away_df], axis=1)
    return merged_df

    


def main():
        team_one = sys.argv[1]
        team_two = sys.argv[2]

        team_one_dict = json.loads(team_one)
        team_two_dict = json.loads(team_two)

        db_connection = connect_to_db()
        cursor = db_connection.cursor()
        cursor.execute("SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")

        errors = prepare_team_data(cursor, team_one_dict, 0)
        errors.extend(prepare_team_data(cursor, team_two_dict, 1))

        if errors:
            results_json = json.dumps({"success": False, "message": " ; ".join(errors)})
            print(results_json)
            return
        



        all_stats_data = get_query(cursor)
        final_df = convert_to_dataframe(all_stats_data)

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

        df_to_scale = final_df[features_columns]
        scaler = joblib.load('scaler2.pkl')

        combined_team_scaled = scaler.transform(df_to_scale)
        combined_team_scaled_tensor = torch.tensor(combined_team_scaled.astype(np.float32))
        
        # Load the model
        nba_model = md.NBA_Score_Predictor_Model(84)
        nba_model.load_state_dict(torch.load('saved_models/model_two.pth'))
        nba_model.eval()
        predicted_scores = nba_model(combined_team_scaled_tensor)
        result_list = predicted_scores.detach().cpu().numpy().tolist()
        home_score = math.ceil(result_list[0][0])
        away_score = math.floor(result_list[0][1])
  
        rounded_result = [home_score, away_score]
        results_json = json.dumps({"home_score": home_score, "away_score": away_score, "success": True})
        print(results_json)
        db_connection.close()


if __name__ == "__main__":
    main()
