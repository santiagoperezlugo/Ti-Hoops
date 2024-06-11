CREATE DATABASE IF NOT EXISTS 2018_data;
USE 2018_data;

CREATE TABLE IF NOT EXISTS teams (
    team_id VARCHAR(15) PRIMARY KEY,
    team_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS games (
    game_id VARCHAR(15) PRIMARY KEY, 
    game_date DATE,
    home_team VARCHAR(15),
    visitor_team VARCHAR(15),
    home_score INT,
    visitor_score INT,
    winner VARCHAR(15),
    loser VARCHAR(15),
    season VARCHAR(10),
    FOREIGN KEY (home_team) REFERENCES teams(team_id),
    FOREIGN KEY (visitor_team) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS player_stats (
    player_id INT PRIMARY KEY, 
    game_id VARCHAR(15),
    team_id VARCHAR(15),
    player_name VARCHAR(100),
    min INT,
    pts INT,
    reb INT,
    ast INT,
    stl INT,
    blk FLOAT,
    tov FLOAT,
    pf FLOAT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS player_season_averages (
    player_id INT,
    season VARCHAR(10),
    team_id VARCHAR(15),
    avg_min FLOAT,
    avg_pts FLOAT,
    avg_reb FLOAT,
    avg_ast FLOAT,
    avg_stl FLOAT,
    avg_blk FLOAT,
    avg_tov FLOAT,
    avg_pf FLOAT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
