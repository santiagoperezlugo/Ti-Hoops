import os
import pandas as pd
import mysql.connector

def getConnection():
    db = mysql.connector.connect(
        host='localhost',
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database='2018_data'
    )
    return db

def get_data():
    connect = getConnection()
    cursor = connect.cursor()

    # Fetch basic game data
    game_query = "SELECT game_id, home_team_id, away_team_id, home_score, away_score, winner_team_id FROM games"
    cursor.execute(game_query)
    games_data = cursor.fetchall()

    # Aggregate player statistics by game and team
    aggregated_stats_query = """
    SELECT 
        team_id, 
        SUM(avg_pts) AS total_points,
        SUM(avg_reb) AS total_rebounds, 
        SUM(avg_ast) AS total_ast,
        SUM(avg_stl) AS total_stl,
        SUM(avg_blk) AS total_blk,
        SUM(avg_tov) AS total_tov,
        SUM(avg_pf) AS total_pf,

        AVG(avg_pts) AS avg_points,
        AVG(avg_reb) AS avg_rebounds, 
        AVG(avg_ast) AS avg_ast,
        AVG(avg_stl) AS avg_stl,
        AVG(avg_blk) AS avg_blk,
        AVG(avg_tov) AS avg_tov,
        AVG(avg_pf) AS avg_pf,

        MAX(avg_pts) AS max_points, 
        MAX(avg_reb) AS max_rebounds,
        MAX(avg_ast) AS max_assists,
        MAX(avg_stl) AS max_steals,
        MAX(avg_blk) AS max_blocks,
        MAX(avg_tov) AS max_turnovers,
        MAX(avg_pf) AS max_pfs,
        MIN(avg_pts) AS min_points,
        
        MIN(avg_reb) AS min_rebounds,
        MIN(avg_ast) AS min_assists,
        MIN(avg_pf) AS min_pfs
    FROM player_season_averages
    GROUP BY team_id
    """
    cursor.execute(aggregated_stats_query)
    aggregated_stats_data = cursor.fetchall()
    connect.close()

    # Combine all data into a single dictionary
    data = {
        'games': games_data,
        'aggregated_stats': aggregated_stats_data
    }
    return data

def convert_to_dataframe(data):
    team_df = pd.DataFrame(data['aggregated_stats'], columns=[
        'team_id', 'total_points', 'total_rebounds', 'total_ast', 'total_stl',
        'total_blk', 'total_tov', 'total_pf', 'avg_points', 'avg_rebounds',
        'avg_ast', 'avg_stl', 'avg_blk', 'avg_tov', 'avg_pf', 'max_points',
        'max_rebounds', 'max_assists', 'max_steals', 'max_blocks', 'max_turnovers',
        'max_pfs', 'min_points', 'min_rebounds', 'min_assists', 'min_pfs'
    ])
    games_df = pd.DataFrame(data['games'], columns=[
        'game_id', 'home_team_id', 'away_team_id', 'home_score', 'away_score', 'winner_team_id'
    ])
    return games_df, team_df

def prepare_model_data(games_df, team_df):
    # Merge with stats for home team
    games_df = games_df.merge(team_df, left_on='home_team_id', right_on='team_id', how='left', suffixes=('', '_home'))

    # Merge with stats for away team
    games_df = games_df.merge(team_df, left_on='away_team_id', right_on='team_id', how='left', suffixes=('_home', '_away'))
    return games_df

# Example usage
def getData():
    data = get_data()
    games_df, team_df = convert_to_dataframe(data)
    model_data = prepare_model_data(games_df, team_df)
    return model_data

# model_data = getData()
# pd.set_option('display.max_columns', None)
# print("\nModel Data DataFrame:")
# print(model_data.head())

# print("\nNull values in Model Data DataFrame:")
# print(model_data.isnull().sum())

# print("\nSummary of Model Data DataFrame:")
# print(model_data.describe())
