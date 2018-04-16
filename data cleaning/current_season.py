import pandas as pd
import numpy as np
import os
import json
import requests
from bs4 import BeautifulSoup
from io import StringIO

# def get_current_players():
#     rootdir = '../resources/players/'
#     player_names = []
#     for subdir, dirs, files in os.walk(rootdir):
#         for file in files:
#             data_path = os.path.join(subdir)
#             name = data_path.replace(rootdir, "")
#             player_names.append(name)
#
#     filename = "../resources/scraped_players.csv"
#     # opening the file with w+ mode truncates the file
#     f = open(filename, "w+")
#     f.close()
#     for path, subdirs, files in os.walk(rootdir):
#         for name in files:
#             if name == 'gw.csv':
#                 trainFile = os.path.join(path, name)
#                 pwd = os.getcwd()
#                 os.chdir(os.path.dirname(trainFile))
#                 df = pd.read_csv(os.path.basename(trainFile), sep=',', skiprows=[0], header=None, encoding='utf-8')
#                 os.chdir(pwd)
#                 with open(filename, 'a') as f:
#                     df.to_csv(f, header=False)
#
# def merge_ids():
#     get_current_players()
#     player_df = pd.read_csv('../resources/scraped_players.csv', sep=',', encoding='utf-8', header=None)
#     id_file = '../resources/player_idlist.csv'
#     ids = pd.read_csv(id_file, sep=',', encoding='utf-8')
#
#     player_df['season'] = '2017/2018'
#     player_df.columns = ['round', 'assists', 'attempted_passes', 'big_chances_created',
#                   'big_chances_missed', 'bonus', 'bps', 'clean_sheets',
#                   'clearances_blocks_interceptions', 'completed_passes', 'creativity',
#                   'dribbles', 'ea_index', 'element', 'errors_leading_to_goal',
#                   'errors_leading_to_goal_attempt', 'fixture', 'fouls', 'goals_conceded',
#                   'goals_scored', 'ict_index', 'id', 'influence', 'key_passes',
#                   'kickoff_time', 'kickoff_time_formatted', 'loaned_in', 'loaned_out',
#                   'minutes', 'offside', 'open_play_crosses', 'opponent_team', 'own_goals',
#                   'penalties_conceded', 'penalties_missed', 'penalties_saved',
#                   'recoveries', 'red_cards', 'round', 'saves', 'selected', 'tackled',
#                   'tackles', 'target_missed', 'team_a_score', 'team_h_score', 'threat',
#                   'total_points', 'transfers_balance', 'transfers_in', 'transfers_out',
#                   'value', 'was_home', 'winning_goals', 'yellow_cards', 'season']
#     player_df.drop(['id'], axis=1, inplace=True)
#     player_df.rename(columns={'element': 'id'}, inplace=True)
#
#     players = player_df.merge(ids, how='left', on=['id'])
#     players.to_csv('../resources/BaseData2017-18.csv', sep=',', encoding='utf-8')
#
# def team_data():
#     merge_ids()
#     raw_file = '../resources/players_raw.csv'
#     players_raw = pd.read_csv(raw_file, sep=',', encoding='utf-8')
#     teams = '../resources/team_codes.csv'
#     team_codes = pd.read_csv(teams, sep=',', encoding='utf-8')
#     team_codes.rename(columns={'team_code': 'team'}, inplace=True)
#     all_teams = players_raw.merge(team_codes, how='left', on=['team'])
#     new = all_teams[['first_name', 'second_name', 'team', 'team_name']].copy()
#
#     cuurent_players_file = '../resources/BaseData2017-18.csv'
#     current_players = pd.read_csv(cuurent_players_file, sep=',', encoding='utf-8')
#
#     merged_players = current_players.merge(new, how='left', on=['first_name', 'second_name'])
#
#     opponent_team_codes = team_codes.copy()
#     opponent_team_codes.rename(columns={'team': 'opponent_team'}, inplace=True)
#     data = merged_players.merge(opponent_team_codes, how='left', on=['opponent_team'])
#     data.rename(columns={'team_name_x': 'team_name', 'team_name_y': 'opponent_team_name'}, inplace=True)
#     data.drop(['Unnamed: 0', 'winning_goals'], axis=1, inplace=True)
#     data.to_csv('../resources/BeforeCreatedFeatures2017-18.csv', sep=',', encoding='utf-8')

def merge_league_ranks():
    # team_data()

    CurrentPlayers = pd.read_csv('../resources/BeforeCreatedFeatures2017-18.csv', sep=',', encoding='utf-8')
    CurrentPlayers.drop(['Unnamed: 0', 'team', 'attempted_passes', 'big_chances_missed', 'bps', 'big_chances_created',
                         'clearances_blocks_interceptions', 'completed_passes', 'dribbles', 'round',
                         'errors_leading_to_goal', 'errors_leading_to_goal_attempt', 'fouls',
                         'kickoff_time', 'kickoff_time_formatted', 'loaned_in', 'loaned_out', 'offside',
                         'open_play_crosses','own_goals', 'penalties_conceded', 'penalties_missed',  'penalties_saved',
                         'recoveries', 'red_cards', 'selected', 'tackled', 'tackles', 'target_missed',
                         'transfers_balance', 'transfers_in', 'transfers_out', 'yellow_cards', 'ea_index'],
                        axis=1, inplace=True)
    CurrentPlayers.rename(columns={'team_name': 'team', 'opponent_team_name': 'opponents', 'second_name': 'name',
                                   'round.1':'round'}, inplace=True)
    CurrentPlayers.replace(['Bournmouth', 'Brighton', 'Huddersfield'], ['AFC Bournemouth', 'Brighton and Hove Albion',
                                                                        'Huddersfield Town'], inplace=True)

    a = 0
    b = 1
    c = 2
    df_list = []

    for i in range(1, 29):
        url = "https://footballapi.pulselive.com/football/standings?compSeasons=79&altIds=true&detail=2&FOOTBALL_COMPETITION=1&gameweekNumbers=1-" + str(
            i)

        r = requests.get(url, headers={"Content-Type": "application/x-www-form-urlencoded", "Connection": "keep-alive",
                                       "Accept": "*/*",
                                       "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US, en; q=0.9",
                                       "Host": "footballapi.pulselive.com", "Origin": "https://www.premierleague.com",
                                       "Referer": "https://www.premierleague.com/tables?co=1&se=79&ha=-1",
                                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
                                       })
        data = json.loads(r.text)

        for x in data['tables']:
            y = x['entries']

        for j in range(0, 20):
            rank_data = y[j]
            position = rank_data["position"]
            team = rank_data['team']
            team_name = team['name']

            df = pd.DataFrame({'gameweek': i, 'position': position, 'name': team_name}, index=[a, b, c])

            df_list.append(df)

            a = a + 1
            b = b + 1
            c = c + 1

    result = pd.concat(df_list)
    result = result.drop_duplicates()
    result.rename(columns={'gameweek': 'round'}, inplace=True)
    result.rename(columns={'name': 'team'}, inplace=True)
    df = pd.merge(CurrentPlayers, result, how='left', left_on=['round', 'team'], right_on=['round', 'team'])
    opponent_ranks = result.rename(columns={'team': 'opponents', 'position': 'opponent_position'})
    merged = pd.merge(df, opponent_ranks, how='left', left_on=['round', 'opponents'], right_on=['round', 'opponents'])
    merged = merged.dropna()
    merged.to_csv('../resources/league_ranks_joined_with_opp.csv', sep=',', encoding='utf-8')

def create_features():
    # merge_league_ranks()

    # merged = pd.read_csv('../resources/league_ranks_joined_with_opp.csv', sep=',', index_col=0, encoding='utf-8')
    # merged['team_goals'] = 0
    # merged['opposition_goals'] = 0
    # team_array = sorted(merged.team.unique())
    # for current_team in team_array:
    #     for index, row in merged.iterrows():
    #         if row.team == current_team:
    #             if row.was_home == True:
    #                 merged.loc[index, 'team_goals'] = row.team_h_score
    #                 merged.loc[index, 'opposition_goals'] = row.team_a_score
    #             else:
    #                 merged.loc[index, 'team_goals'] = row.team_a_score
    #                 merged.loc[index, 'opposition_goals'] = row.team_h_score
    #
    # merged.drop(['team_h_score', 'team_a_score'], axis=1, inplace=True)
    # merged.to_csv('../resources/team_goals.csv', sep=',', encoding='utf-8')
    #
    df_array = []
    team_counter = 1
    merged = pd.read_csv('../resources/team_goals.csv', sep=',', index_col=0, encoding='utf-8')
    team_array = sorted(merged.team.unique())
    for current_team in team_array:
        tempDF = merged.loc[merged['team'] == current_team]

        home_count = 0
        home_goals = 0
        away_count = 0
        away_goals = 0
        tempDF2 = tempDF.copy(deep=True)
        tempDF2.drop_duplicates(subset='round', inplace=True)
        tempDF2.sort_values('round', ascending=True, inplace=True)
        for index, row in tempDF2.iterrows():
            if row.was_home == True:
                home_count += 1
                home_goals += row.team_goals
                tempDF2.loc[index, 'team_pot'] =  (home_goals / home_count)
            else:
                away_count += 1
                away_goals += row.team_goals
                tempDF2.loc[index, 'team_pot'] = (away_goals / away_count)

        keys = tempDF2['round']
        values = tempDF2['team_pot']
        dictionary = dict(zip(keys, values))
        for index, row in tempDF.iterrows():
            if row.team == current_team:
                for key, value in dictionary.items():
                    if key == row['round']:
                        tempDF.loc[index, 'team_pot'] = value

        home_count = 0
        home_goals = 0
        away_count = 0
        away_goals = 0
        for index, row in tempDF2.iterrows():
            if row.was_home == True:
                home_count += 1
                home_goals += row.opposition_goals
                tempDF2.loc[index, 'concede_pot'] = (home_goals / home_count)
            else:
                away_count += 1
                away_goals += row.opposition_goals
                tempDF2.loc[index, 'concede_pot'] = (away_goals / away_count)

        keys = tempDF2['round']
        values = tempDF2['concede_pot']
        dictionary = dict(zip(keys, values))

        for index, row in tempDF.iterrows():
            for key, value in dictionary.items():
                if tempDF.loc[index, 'round'] == key:
                    tempDF.loc[index, 'concede_pot'] = value

        globals()['team{}'.format(team_counter)] = tempDF
        df_array.append(globals()['team{}'.format(team_counter)])
        team_counter += 1
        print(current_team)

    Players = pd.concat(df_array)
    Players.drop_duplicates(subset=['id', 'round'], inplace=True)
    Players.sort_values(['id', 'round'], ascending=True, inplace=True)

    team_pots = []
    concede_pots = []
    for team in df_array:
        team.drop_duplicates(subset='round', inplace=True)
        team.sort_values('round', ascending=True, inplace=True)
        keys = team['round']
        values = team['team_pot']
        dictionary = dict(zip(keys, values))
        team_pots.append(dictionary)

    for team in df_array:
        team.drop_duplicates(subset='round', inplace=True)
        team.sort_values('round', ascending=True, inplace=True)
        keys = team['round']
        values = team['concede_pot']
        dictionary = dict(zip(keys, values))
        concede_pots.append(dictionary)

    for index, row in Players.iterrows():
        for key, value in team_pots[0].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'AFC Bournemouth':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[0].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'AFC Bournemouth':
                    Players.loc[index, 'opp_concede_pot'] =  value


    for index, row in Players.iterrows():
        for key, value in team_pots[1].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Arsenal':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[1].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Arsenal':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[2].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Brighton and Hove Albion':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[2].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Brighton and Hove Albion':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[3].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Burnley':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[3].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Burnley':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[4].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Chelsea':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[4].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Chelsea':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[5].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Crystal Palace':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[5].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Crystal Palace':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[6].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Everton':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[6].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Everton':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[7].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Huddersfield Town':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[7].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Huddersfield Town':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[8].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Leicester City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[8].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Leicester City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[9].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Liverpool':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[9].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Liverpool':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[10].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[10].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[11].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester United':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[11].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester United':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[12].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Newcastle United':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[12].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Newcastle United':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[13].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Southampton':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[13].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Southampton':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[14].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Stoke City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[14].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Stoke City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[15].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Swansea City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[15].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Swansea City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[16].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Tottenham Hotspur':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[16].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Tottenham Hotspur':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[17].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Watford':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[17].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Watford':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[18].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'West Bromwich Albion':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[18].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'West Bromwich Albion':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[19].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'West Ham United':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[19].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'West Ham United':
                    Players.loc[index, 'opp_concede_pot'] = value
    # Players.to_csv('../resources/team_pots.csv', sep=',', encoding='utf-8')

    # Players = pd.read_csv('../resources/team_pots.csv', sep=',', index_col=0, encoding='utf-8')
    Players = Players[Players['minutes'] > 0]
    Players['form_points'] = Players.groupby('id')['total_points'].apply(
        lambda x: x.rolling(center=False, window=3).mean())
    Players = Players.fillna(0)
    Players['ict_form'] = Players.groupby('id')['ict_index'].apply(
        lambda x: x.rolling(center=False, window=3).mean())
    Players = Players.fillna(0)
    Players['save_form'] = Players.groupby('id')['saves'].apply(
        lambda x: x.rolling(center=False, window=3).mean())
    Players = Players.fillna(0)
    Players['long_form'] = Players.groupby('id')['total_points'].apply(
        lambda x: x.rolling(center=False, window=5).mean())
    Players = Players.fillna(0)
    temp = Players.copy()

    playerIDs = sorted(Players.id.unique())
    for player in playerIDs:
        for i, row in temp.iterrows():
            if temp.loc[i, 'id'] == player:
                temp['prev_points'] = temp.groupby('id')['total_points'].shift()
    temp = temp.fillna(0)
    temp.to_csv('../resources/Dfeatures.csv', sep=',', encoding='utf-8')
create_features()

