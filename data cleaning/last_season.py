import pandas as pd
import numpy as np

def clean_last_season():
    fantasy_data = pd.read_csv('../resources/1617playerdata.csv', sep=',', encoding='utf-8')
    league_ranks = pd.read_csv('../resources/team_ranks.csv', sep=',', encoding='utf-8')

    league_ranks.rename(columns={'Club': 'team', 'More':'round'}, inplace=True)
    league_ranks.drop(['Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points'], axis=1, inplace=True)
    league_ranks['Position'] = league_ranks['Position'].str[0:2]
    x = 1
    for i in range(0, 760, 20):
        j = i + 20
        league_ranks.iloc[i:j, league_ranks.columns.get_loc('round')] = x
        x = x + 1

    merged = pd.merge(fantasy_data, league_ranks, how='left', left_on = ['round','team'], right_on = ['round','team'])
    merged.drop('Unnamed: 0', axis=1, inplace=True)
    merged.rename(columns={'Position': 'team_rank'}, inplace=True)
    league_ranks.rename(columns={'team': 'opponents'}, inplace=True)
    merged = pd.merge(merged, league_ranks, how='left', left_on=['round', 'opponents'], right_on=['round', 'opponents'])
    merged.rename(columns={'Position': 'opponent_team_rank'}, inplace=True)
    merged.replace('H', True, inplace=True)
    merged.replace('A', False, inplace=True)
    merged['season'] = '2016/17'

    df_array = []
    team_counter = 1
    team_array = sorted(merged.team.unique())
    merged.rename(columns={'venue': 'was_home'}, inplace=True)
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
                tempDF2.loc[index, 'team_pot'] = (home_goals / home_count)
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
    Players.drop_duplicates(subset=['player_id', 'round'], inplace=True)
    Players.sort_values(['player_id', 'round'], ascending=True, inplace=True)
    # Players.to_csv('../resources/last_season_pots.csv', sep=',', encoding='utf-8')


    # Players = pd.read_csv('../resources/last_season_pots.csv', sep=',', encoding='utf-8')
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
                if Players.loc[index, 'opponents'] == 'Arsenal':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[0].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Arsenal':
                    Players.loc[index, 'opp_concede_pot'] =  value


    for index, row in Players.iterrows():
        for key, value in team_pots[1].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Bournemouth':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[1].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Bournemouth':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[2].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Burnley':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[2].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Burnley':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[3].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Chelsea':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[3].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Chelsea':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[4].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Crystal Palace':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[4].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Crystal Palace':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[5].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Everton':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[5].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Everton':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[6].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Hull City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[6].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Hull City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[7].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Leicester City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[7].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Leicester City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[8].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Liverpool':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[8].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Liverpool':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[9].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[9].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[10].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester United':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[10].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Manchester United':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[11].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Middlesbrough':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[11].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Middlesbrough':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[12].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Southampton':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[12].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Southampton':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[13].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Stoke City':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[13].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Stoke City':
                    Players.loc[index, 'opp_concede_pot'] = value

    for index, row in Players.iterrows():
        for key, value in team_pots[14].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Sunderland':
                    Players.loc[index, 'opp_pot'] = value
        for key, value in concede_pots[14].items():
            if Players.loc[index, 'round'] == key:
                if Players.loc[index, 'opponents'] == 'Sunderland':
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
    Players['form_points'] = Players.groupby('player_id')['total_points'].apply(
        lambda x: x.rolling(center=False, window=3).mean())
    Players = Players.fillna(0)
    Players['ict_form'] = Players.groupby('player_id')['ict_index'].apply(
        lambda x: x.rolling(center=False, window=3).mean())
    Players = Players.fillna(0)
    Players['save_form'] = Players.groupby('player_id')['saves'].apply(
        lambda x: x.rolling(center=False, window=3).mean())
    Players = Players.fillna(0)
    Players['long_form'] = Players.groupby('player_id')['total_points'].apply(
        lambda x: x.rolling(center=False, window=5).mean())
    Players = Players.fillna(0)
    temp = Players.copy()

    playerIDs = sorted(Players.player_id.unique())
    for player in playerIDs:
        for i, row in temp.iterrows():
            if temp.loc[i, 'player_id'] == player:
                temp['prev_points'] = temp.groupby('player_id')['total_points'].shift()
    temp = temp.fillna(0)
    temp.to_csv('../resources/last_seasonFeatures.csv', sep=',', encoding='utf-8')

    LastSeason = pd.read_csv('../resources/last_seasonFeatures.csv', sep=',', encoding='utf-8', index_col=0)
    CurrentSeason = pd.read_csv('../resources/Dfeatures.csv', sep=',', encoding='utf-8', index_col=0)


clean_last_season()

