import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamelog

# Setting display option
pd.set_option('display.max_columns', None)

# Get game logs for the 1985-86 NBA regular season
# games_finder = leaguegamelog.LeagueGameLog(season='1988-89', league_id='00', player_or_team_abbreviation='T', season_type_all_star='Regular Season')
# games_df = games_finder.get_data_frames()[0]
# print(games_df.head())

# # Extract unique teams with their acronyms and team IDs from the games DataFrame
# unique_teams = games_df[['TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION']].drop_duplicates()
# print(unique_teams)
# old_teams = {name: abbr for name, abbr in zip(unique_teams['TEAM_NAME'], unique_teams['TEAM_ABBREVIATION'])}

# nba_teams = teams.get_teams()
# team_acronyms = {}
# for team in nba_teams:
#     print('team id: ', team['id'], 'team_name: ', team['full_name'], 'acronym : ', team['abbreviation'])
#     team_acronyms[team['full_name']] = team['abbreviation']

# diff_keys = set(old_teams.keys()) ^ set(team_acronyms.keys())
# diff_values = []

# for key in set(old_teams.keys()) & set(team_acronyms.keys()):
#     if old_teams[key] != team_acronyms[key]:
#         diff_values.append((key, old_teams[key], team_acronyms[key]))

# print("Keys present in old teams but not the other:")
# print(diff_keys)

# print("\nKey-value pairs with different values:")
# for key, value1, value2 in diff_values:
#     print(f"Key: {key}, Value in old teams: {value1}, Value in new teams: {value2}")


games_finder = leaguegamelog.LeagueGameLog(season='1988-89', league_id='00', player_or_team_abbreviation='T', season_type_all_star='Regular Season')
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
    home_team_id = game['TEAM_ID']
    away_team_id = game_away['TEAM_ID']
    print(home_team, away_team, home_team_id, away_team_id)