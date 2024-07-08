import mysql.connector
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, playergamelogs, leaguegamelog
import os
import pandas as pd

def fetchGamesForSeason(season, cursor, db_connection):
    games_finder = leaguegamelog.LeagueGameLog(season=season, league_id='00', player_or_team_abbreviation='T', season_type_all_star='Regular Season')
    games_df = games_finder.get_data_frames()[0]
    grouped_games = games_df.groupby('GAME_ID')

    for game_id, group in grouped_games:
        if len(group) != 2:
            continue 

        group = group.sort_values(by='MATCHUP')
        game = group.iloc[0]  # Home team info
        game_away = group.iloc[1]  # away team info

        home_team = game['TEAM_ABBREVIATION']
        away_team = game_away['TEAM_ABBREVIATION']
        home_score = int(game['PTS'])
        away_score = int(game_away['PTS'])

        # Determine winner and loser
        winner = home_team if game['WL'] == 'W' else away_team
        home_team_id = int(game['TEAM_ID'])
        away_team_id = int(game_away['TEAM_ID'])
       
        if winner == home_team:
            winner_team_id = home_team_id
        if winner == away_team:
            winner_team_id = away_team_id

        
        if home_team_id is None or away_team_id is None:
            print(f"Team ID not found for: home_team {home_team}, away_team {away_team}")
            continue


        sql = """
        INSERT INTO games (game_id, game_date, home_team_id, away_team_id, home, away, home_score, away_score, winner_team_id, winner, season)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE
        game_date = VALUES(game_date), home_team_id = VALUES(home_team_id), away_team_id = VALUES(away_team_id),
        home = VALUES(home), away = VALUES(away), home_score = VALUES(home_score), away_score = VALUES(away_score),
        winner_team_id = VALUES(winner_team_id), winner = VALUES(winner)
        """
        game_data = (
            game['GAME_ID'], game['GAME_DATE'], home_team_id, away_team_id,
            home_team, away_team, home_score, away_score, winner_team_id, winner, season
            )

        try:
            cursor.execute(sql, game_data)
        except mysql.connector.Error as err:
            print(f"Failed to insert game {game['GAME_ID']}: {err}")
            
    db_connection.commit()


def fetchPlayersforSeason(season, cursor, db_connection):
    player_logs = playergamelogs.PlayerGameLogs(season_nullable=season, season_type_nullable='Regular Season')
    players = player_logs.get_data_frames()[0]
    cursor.execute("TRUNCATE TABLE player_stats")

    for index, player in players.iterrows():
        sql = """
        INSERT INTO player_stats (player_id, game_id, team_id, player_name, min, pts, fg_pct, reb, ast, stl, blk, tov, pf, plus_minus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        min = VALUES(min), pts = VALUES(pts), fg_pct = VALUES(fg_pct), reb = VALUES(reb), ast = VALUES(ast),
        stl = VALUES(stl), blk = VALUES(blk), tov = VALUES(tov), pf = VALUES(pf), plus_minus = VALUES(plus_minus)
        """

        if player['PLUS_MINUS'] is None:
            player['PLUS_MINUS'] = 0
        player_data = (
            player['PLAYER_ID'], player['GAME_ID'], player['TEAM_ID'], player['PLAYER_NAME'].upper(),
            player['MIN'], player['PTS'], player['FG_PCT'], player['REB'], player['AST'], player['STL'], 
            player['BLK'], player['TOV'], player['PF'], player['PLUS_MINUS']
        )
        try:
            cursor.execute(sql, player_data)
        except mysql.connector.Error as err:
            print(f"Failed to insert player stats for {player['PLAYER_ID']} in game {player['GAME_ID']}: {err}")

    db_connection.commit()


def fetchTeamsforSeason(cursor, db_connection):
    nba_teams = teams.get_teams()
    for team in nba_teams:
        sql = """
        INSERT INTO teams (team_id, team_name, team_abbreviation)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE team_name = VALUES(team_name), team_abbreviation = VALUES(team_abbreviation)
        """
        team_data = (team['id'], team['full_name'].upper(), team['abbreviation'])
        try:
            cursor.execute(sql, team_data)
        except mysql.connector.Error as err:
            print("Failed to insert team {team['id']}: {err}")
    print("Teams inserted successfully")
    db_connection.commit()




def fetchPlayerSeasonAverages(season, cursor, db_connection):
    sql_select = """
    SELECT player_id, player_name, AVG(min) AS avg_min, AVG(pts) AS avg_pts, AVG(fg_pct) AS avg_fg_pct,
            AVG(reb) AS avg_reb, AVG(ast) AS avg_ast, AVG(stl) AS avg_stl, AVG(blk) AS avg_blk,
            AVG(tov) AS avg_tov, AVG(pf) AS avg_pf, AVG(plus_minus) AS avg_plus_minus, team_id
    FROM player_stats
    WHERE game_id IN (SELECT game_id FROM games WHERE season = %s)
    GROUP BY player_id, player_name, team_id
    """
    cursor.execute(sql_select, (season,))
    results = cursor.fetchall()


    sql_insert = """
    INSERT INTO player_season_averages
    (player_id, player_name, season, team_id, avg_min, avg_pts, avg_fg_pct, avg_reb, avg_ast, avg_stl,
     avg_blk, avg_tov, avg_pf, avg_plus_minus)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    avg_min = VALUES(avg_min), avg_pts = VALUES(avg_pts), avg_fg_pct = VALUES(avg_fg_pct),
    avg_reb = VALUES(avg_reb), avg_ast = VALUES(avg_ast), avg_stl = VALUES(avg_stl), 
    avg_blk = VALUES(avg_blk), avg_tov = VALUES(avg_tov), avg_pf = VALUES(avg_pf), avg_plus_minus = VALUES(avg_plus_minus)
    """
    for result in results:
        player_id, player_name, avg_min, avg_pts, avg_fg_pct, avg_reb, avg_ast, avg_stl, avg_blk, avg_tov, avg_pf, avg_plus_minus, team_id = result
        cursor.execute(sql_insert, (player_id, player_name, season, team_id, avg_min, avg_pts, avg_fg_pct, avg_reb, avg_ast, avg_stl, avg_blk, avg_tov, avg_pf, avg_plus_minus))

    db_connection.commit()




def insert_data_into_sql(year, cursor, database_connect):
    fetchTeamsforSeason(cursor, database_connect)  
    fetchGamesForSeason(year, cursor, database_connect)  
    fetchPlayersforSeason(year, cursor, database_connect) 
    fetchPlayerSeasonAverages(year, cursor, database_connect)
