import os
import pandas as pd
import mysql.connector

def get_data(cursor):
    game_query = "SELECT game_id, home_team_id, away_team_id, home_score, away_score, winner_team_id, season FROM games"
    cursor.execute(game_query)
    games_data = cursor.fetchall()

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
        FROM player_season_averages
        GROUP BY season, team_id;
    """

    cursor.execute(aggregated_stats_query)
    aggregated_stats_data = cursor.fetchall()

    data = {
        'games': games_data,
        'aggregated_stats': aggregated_stats_data
    }
    return data

def convert_to_dataframe(data):
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

    team_df = pd.DataFrame(data['aggregated_stats'], columns=columns)
    team_df[columns] = team_df[columns].fillna(0)
    games_df = pd.DataFrame(data['games'], columns=[
        'game_id', 'home_team_id', 'away_team_id', 'home_score', 'away_score', 'winner_team_id', 'season'
    ])
    return games_df, team_df


def prepare_model_data(games_df, team_df):
    games_df = games_df.merge(team_df, left_on=['home_team_id', 'season'], right_on=['team_id', 'season'], how='left', suffixes=('', '_home'))
    games_df = games_df.merge(team_df, left_on=['away_team_id', 'season'], right_on=['team_id', 'season'], how='left', suffixes=('_home', '_away'))
    games_df.drop(columns=['team_id_home', 'team_id_away', 'season', 'game_id', 'home_team_id', 'away_team_id'], inplace=True)
    pd.set_option('display.max_columns', None)
    return games_df


def getData(cursor):
    data = get_data(cursor)
    games_df, team_df = convert_to_dataframe(data)
    model_data = prepare_model_data(games_df, team_df)
    return model_data
