import mysql.connector
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, playergamelogs, leaguegamelog
import os

def connectToDB():
    host = 'localhost'
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = '2018_data'

    print(f"Connecting to database {database} on {host} as {user}")
    
    try:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None



def fetchGamesForSeason(season, cursor, db_connection):
    games_finder = leaguegamelog.LeagueGameLog(season=season, league_id='00', player_or_team_abbreviation='T', season_type_all_star='Regular Season')
    games_df = games_finder.get_data_frames()[0] #returns data as pandas dataframe

    grouped_games = games_df.groupby('GAME_ID')

    for game_id, group in grouped_games:
        if len(group) != 2:
            continue  # Skip any game not having exactly two entries

        group = group.sort_values(by='MATCHUP')
        game = group.iloc[0]  # Home team info
        game_away = group.iloc[1]  # away team info

        home_team = game['TEAM_ABBREVIATION']
        away_team = game_away['TEAM_ABBREVIATION']
        home_score = int(game['PTS'])
        away_score = int(game_away['PTS'])

        # Determine winner and loser
        winner = home_team if game['WL'] == 'W' else away_team

        # Ensure we have valid team IDs
        cursor.execute("SELECT team_id FROM teams WHERE team_abbreviation = %s", (home_team,))
        home_team_id = cursor.fetchone()
        cursor.execute("SELECT team_id FROM teams WHERE team_abbreviation = %s", (away_team,))
        away_team_id = cursor.fetchone()

        cursor.execute("SELECT team_id FROM teams WHERE team_abbreviation = %s", (winner,))
        winner_team_id = cursor.fetchone()

        
        if home_team_id is None or away_team_id is None:
            print(f"Team ID not found for: home_team {home_team}, away_team {away_team}")
            continue

        home_team_id = int(home_team_id[0])
        away_team_id = int(away_team_id[0])
        winner_team_id = int(winner_team_id[0])


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
    # Initialize the PlayerGameLogs with appropriate parameters
    player_logs = playergamelogs.PlayerGameLogs(season_nullable=season, season_type_nullable='Regular Season')
    players = player_logs.get_data_frames()[0]

    for index, player in players.iterrows():
        sql = """
        INSERT INTO player_stats (player_id, game_id, team_id, player_name, min, pts, reb, ast, stl, blk, tov, pf)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        player_id = VALUES(player_id), game_id = VALUES(game_id), team_id = VALUES(team_id),
        min = VALUES(min), pts = VALUES(pts), reb = VALUES(reb), ast = VALUES(ast),
        stl = VALUES(stl), blk = VALUES(blk), tov = VALUES(tov), pf = VALUES(pf)
        """
        player_data = (
            player['PLAYER_ID'], player['GAME_ID'], player['TEAM_ID'], player['PLAYER_NAME'],
            player['MIN'], player['PTS'], player['REB'], player['AST'], player['STL'], 
            player['BLK'], player['TOV'], player['PF']
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
        team_data = (team['id'], team['full_name'], team['abbreviation'])
        try:
            cursor.execute(sql, team_data)
        except mysql.connector.Error as err:
            print("Failed to insert team {team['id']}: {err}")
    print("Teams inserted successfully")
    db_connection.commit()

def fetchPlayerSeasonAverages(season, cursor, db_connection):
    sql_select = """
    SELECT player_id, player_name, AVG(min) AS avg_min, AVG(pts) AS avg_pts, AVG(reb) AS avg_reb,
           AVG(ast) AS avg_ast, AVG(stl) AS avg_stl, AVG(blk) AS avg_blk,
           AVG(tov) AS avg_tov, AVG(pf) AS avg_pf, team_id
    FROM player_stats
    WHERE game_id IN (SELECT game_id FROM games WHERE season = %s)
    GROUP BY player_id, player_name, team_id  # Added player_name here
    """
    cursor.execute(sql_select, (season,))
    results = cursor.fetchall()

    sql_insert = """
    INSERT INTO player_season_averages
    (player_id, player_name, season, team_id, avg_min, avg_pts, avg_reb, avg_ast, avg_stl,
     avg_blk, avg_tov, avg_pf)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    avg_min = VALUES(avg_min), avg_pts = VALUES(avg_pts), avg_reb = VALUES(avg_reb),
    avg_ast = VALUES(avg_ast), avg_stl = VALUES(avg_stl), avg_blk = VALUES(avg_blk),
    avg_tov = VALUES(avg_tov), avg_pf = VALUES(avg_pf)
    """
    for result in results:
        player_id, player_name, avg_min, avg_pts, avg_reb, avg_ast, avg_stl, avg_blk, avg_tov, avg_pf, team_id = result
        cursor.execute(sql_insert, (player_id, player_name, season, team_id, avg_min, avg_pts, avg_reb, avg_ast, avg_stl, avg_blk, avg_tov, avg_pf))

    db_connection.commit()
    print(f"Player season averages for {season} season have been updated in the database.")

database_connect = connectToDB()
if database_connect is None:
    raise SystemExit("Database connection could not be established")

cursor = database_connect.cursor()

fetchTeamsforSeason(cursor, database_connect)  
fetchGamesForSeason("2018-19", cursor, database_connect)  
fetchPlayersforSeason("2018-19", cursor, database_connect) 
fetchPlayerSeasonAverages("2018-19", cursor, database_connect)

cursor.close()
database_connect.close()
