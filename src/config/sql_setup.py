import mysql.connector
import os

def create_tables(cursor):
    # Commands to create database and tables
    commands = [
        "CREATE DATABASE IF NOT EXISTS nba_data;",
        "USE nba_data;",
        """
        CREATE TABLE IF NOT EXISTS teams (
            team_id VARCHAR(15) PRIMARY KEY,
            team_name VARCHAR(50),
            team_abbreviation VARCHAR(3)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS games (
            game_id VARCHAR(15) PRIMARY KEY, 
            game_date DATE,
            home_team_id VARCHAR(15),
            away_team_id VARCHAR(15),
            home VARCHAR(3),
            away VARCHAR(3),
            home_score INT,
            away_score INT,
            winner_team_id VARCHAR(15),
            winner VARCHAR(3),
            loser VARCHAR(15),
            season VARCHAR(10),
            FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS player_stats (
            player_id INT, 
            game_id VARCHAR(15),
            team_id VARCHAR(15),
            player_name VARCHAR(100),
            min INT,
            pts INT,
            fg_pct FLOAT,
            reb INT,
            ast INT,
            stl INT,
            blk FLOAT,
            tov FLOAT,
            pf FLOAT,
            plus_minus FLOAT,
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS player_season_averages (
            player_id INT,
            player_name VARCHAR(100),
            season VARCHAR(10),
            team_id VARCHAR(15),
            avg_min FLOAT,
            avg_pts FLOAT,
            avg_fg_pct FLOAT,
            avg_reb FLOAT,
            avg_ast FLOAT,
            avg_stl FLOAT,
            avg_blk FLOAT,
            avg_tov FLOAT,
            avg_pf FLOAT,
            avg_plus_minus FLOAT,
            PRIMARY KEY (player_id, season, team_id),
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS matchup (
			team_id INT,
            player_name VARCHAR(100),
            season VARCHAR(10),
            avg_pts FLOAT,
            avg_fg_pct FLOAT,
            avg_reb FLOAT,
            avg_ast FLOAT,
            avg_stl FLOAT,
            avg_blk FLOAT,
            avg_tov FLOAT,
            avg_pf FLOAT,
            avg_plus_minus INT,
            PRIMARY KEY (player_name, season, team_id)
        );
        """
    ]
    try:
        for command in commands:
            cursor.execute(command)
        print("Database and tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error executing SQL command: {err}")
