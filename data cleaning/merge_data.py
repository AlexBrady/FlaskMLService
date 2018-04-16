import pandas as pd
import numpy as np

def merge_data():
    LastSeason = pd.read_csv('../resources/last_seasonFeatures.csv', sep=',', encoding='utf-8', index_col=0)
    CurrentSeason = pd.read_csv('../resources/Dfeatures.csv', sep=',', encoding='utf-8', index_col=0)
    CurrentSeason.rename(columns={'position': 'team_rank', 'opponent_position': 'opponent_team_rank'}, inplace=True)

    CurrentSeason.rename(columns={'id': 'player_id'}, inplace=True)
    mapping_df = pd.read_csv('../resources/players_raw.csv', sep=',', encoding='utf-8')
    mapping_df = mapping_df[['id', 'element_type']]
    mapping_df['pos'] = 'pos'
    goalkeeper = 'Goalkeeper'
    defender = 'Defender'
    mid = 'Midfielder'
    forward = 'Forward'

    for index, row in mapping_df.iterrows():
        if row.element_type == 1:
            mapping_df.set_value(index, 'pos', goalkeeper)
        elif row.element_type == 2:
            mapping_df.set_value(index, 'pos', defender)
        elif row.element_type == 3:
            mapping_df.set_value(index, 'pos', mid)
        elif row.element_type == 4:
            mapping_df.set_value(index, 'pos', forward)
    mapping_df.drop('element_type', axis=1, inplace=True)
    mapping_df.rename(columns={'id': 'player_id'}, inplace=True)

    df = pd.merge(CurrentSeason, mapping_df, how='left', left_on=['player_id'], right_on=['player_id'])
    last = LastSeason[['player_id', 'name', 'team', 'pos', 'round', 'opponents', 'was_home', 'team_rank',
                       'opponent_team_rank', 'team_goals', 'opposition_goals', 'total_points', 'minutes',
                       'goals_scored', 'assists', 'clean_sheets', 'saves', 'bonus',
                       'ict_index', 'value', 'season', 'team_pot', 'concede_pot',
                       'opp_pot', 'opp_concede_pot', 'form_points', 'prev_points']]
    df.drop(
        ['creativity', 'first_name', 'fixture', 'goals_conceded', 'influence', 'key_passes', 'opponent_team', 'threat'],
        axis=1, inplace=True)
    dfarray = [df, last]
    MergedData = pd.concat(dfarray)
    print(MergedData.isna().sum())
    MergedData.to_csv('../resources/merged.csv', sep=',', encoding='utf-8')

merge_data()