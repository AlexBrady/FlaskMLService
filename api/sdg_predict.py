import math
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn import svm

def get_midfielders():
    data = pd.read_csv('../resources/merged.csv', sep=',', encoding='utf-8', index_col=0)
    model = data[['player_id', 'name', 'season', 'pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
                  'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points',
                  'long_form', 'ict_form']]

    MidfielderModal = model.loc[model['pos'] == 'Midfielder']
    MidfielderModal.drop('pos', axis=1, inplace=True)
    MidfielderModal.sort_values(['season', 'round'], ascending=True, inplace=True)
    MidfielderModal.to_csv('../resources/predictions/MIDFIELDERS.csv', sep=',', encoding='utf-8')
    players = MidfielderModal[8308:]

    keys = MidfielderModal['round']
    values = pd.cut(MidfielderModal['round'], 3, labels=[1, 2, 3])
    dictionary = dict(zip(keys, values))
    MidfielderModal['round'] = values

    X = MidfielderModal.drop(['total_points', 'season', 'player_id', 'name'], axis=1)
    y = MidfielderModal[['total_points']]

    X_train = X[:8307]
    X_test = X[8308:]
    y_train = y[:8307]
    y_test = y[8308:]

    regression_model = SGDRegressor()
    regression_model.fit(X_train, y_train)

    score = regression_model.score(X_test, y_test)
    y_pred = regression_model.predict(X_test)

    testing = pd.concat([X_test, y_test], 1)
    testing['Predicted'] = np.round(y_pred, 1)
    testing['Prediction_Error'] = testing['total_points'] - testing['Predicted']
    testing['player_id'] = 0
    testing['name'] = 0
    testing['player_id'] = players.player_id
    testing['name'] = players.name
    testing.to_csv('../resources/predictions/MID_PREDS.csv', sep=',', encoding='utf-8')
    # return testing[testing['name'] == name]

# get_midfielders()

def get_defenders():
    data = pd.read_csv('../resources/merged.csv', sep=',', encoding='utf-8', index_col=0)
    model = data[
        ['player_id', 'name', 'season', 'pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
         'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points',
         'long_form', 'ict_form']]

    DefenderModal = model.loc[model['pos'] == 'Defender']
    DefenderModal.drop('pos', axis=1, inplace=True)
    DefenderModal.sort_values(['season', 'round'], ascending=True, inplace=True)
    DefenderModal.to_csv('../resources/predictions/DEFENDERS.csv', sep=',', encoding='utf-8')
    players = DefenderModal[6008:]

    keys = DefenderModal['round']
    values = pd.cut(DefenderModal['round'], 3, labels=[1, 2, 3])
    dictionary = dict(zip(keys, values))
    DefenderModal['round'] = values

    X = DefenderModal.drop(['total_points', 'season', 'long_form', 'team_pot', 'opp_concede_pot', 'player_id', 'name'],
                           axis=1)
    y = DefenderModal[['total_points']]

    X_train = X[:6007]
    X_test = X[6008:]
    y_train = y[:6007]
    y_test = y[6008:]

    regression_model = SGDRegressor()
    regression_model.fit(X_train, y_train)

    score = regression_model.score(X_test, y_test)
    y_pred = regression_model.predict(X_test)

    testing = pd.concat([X_test, y_test], 1)
    testing['Predicted'] = np.round(y_pred, 1)
    testing['Prediction_Error'] = testing['total_points'] - testing['Predicted']
    testing['Prediction_Error'] = testing['Prediction_Error'].abs()
    testing['player_id'] = 0
    testing['name'] = 0
    testing['player_id'] = players.player_id
    testing['name'] = players.name

    print(testing['Prediction_Error'].mean())
    testing.to_csv('../resources/predictions/DEF_PREDS.csv', sep=',', encoding='utf-8')

# get_defenders()

def get_goalkeepers():
    data = pd.read_csv('../resources/merged.csv', sep=',', encoding='utf-8', index_col=0)
    model = data[
        ['player_id', 'name', 'season', 'pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
         'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points', 'save_form',
         'long_form', 'ict_form']]

    GoalkeeperModal = model.loc[model['pos'] == 'Goalkeeper']
    GoalkeeperModal.drop('pos', axis=1, inplace=True)
    GoalkeeperModal.sort_values(['season', 'round'], ascending=True, inplace=True)
    GoalkeeperModal.to_csv('../resources/predictions/GOALKEEPERS.csv', sep=',', encoding='utf-8')
    players = GoalkeeperModal[1354:]

    keys = GoalkeeperModal['round']
    values = pd.cut(GoalkeeperModal['round'], 3, labels=[1, 2, 3])
    dictionary = dict(zip(keys, values))
    GoalkeeperModal['round'] = values

    X = GoalkeeperModal.drop(
        ['total_points', 'season', 'long_form', 'team_pot', 'opp_concede_pot', 'player_id', 'name'], axis=1)
    y = GoalkeeperModal[['total_points']]

    X_train = X[:1353]
    X_test = X[1354:]
    y_train = y[:1353]
    y_test = y[1354:]

    regression_model = SGDRegressor()
    regression_model.fit(X_train, y_train)

    score = regression_model.score(X_test, y_test)
    y_pred = regression_model.predict(X_test)

    testing = pd.concat([X_test, y_test], 1)
    testing['Predicted'] = np.round(y_pred, 1)
    testing['Prediction_Error'] = testing['total_points'] - testing['Predicted']
    # testing['Prediction_Error'] = testing['Prediction_Error'].abs()
    testing['player_id'] = 0
    testing['name'] = 0
    testing['player_id'] = players.player_id
    testing['name'] = players.name

    testing.to_csv('../resources/predictions/GOALK_PREDS.csv', sep=',', encoding='utf-8')

# get_goalkeepers()

def get_forwards():
    data = pd.read_csv('../resources/merged.csv', sep=',', encoding='utf-8', index_col=0)
    model = data[
        ['player_id', 'name', 'season', 'pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
         'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points',
         'long_form', 'ict_form']]

    ForwardModal = model.loc[model['pos'] == 'Forward']
    ForwardModal.drop('pos', axis=1, inplace=True)
    ForwardModal.sort_values(['season', 'round'], ascending=True, inplace=True)
    ForwardModal.to_csv('../resources/predictions/FORWARDS.csv', sep=',', encoding='utf-8')
    players = ForwardModal[2791:]

    keys = ForwardModal['round']
    values = pd.cut(ForwardModal['round'], 3, labels=[1, 2, 3])
    dictionary = dict(zip(keys, values))
    ForwardModal['round'] = values

    X = ForwardModal.drop(['total_points', 'season', 'long_form', 'team_pot', 'opp_concede_pot', 'player_id', 'name'],
                          axis=1)
    y = ForwardModal[['total_points']]

    X_train = X[:2791]
    X_test = X[2790:]
    y_train = y[:2791]
    y_test = y[2790:]

    regression_model = SGDRegressor()
    regression_model.fit(X_train, y_train)

    score = regression_model.score(X_test, y_test)
    y_pred = regression_model.predict(X_test)

    testing = pd.concat([X_test, y_test], 1)
    testing['Predicted'] = np.round(y_pred, 1)
    testing['Prediction_Error'] = testing['total_points'] - testing['Predicted']
    # testing['Prediction_Error'] = testing['Prediction_Error'].abs()
    testing['player_id'] = 0
    testing['name'] = 0
    testing['player_id'] = players.player_id
    testing['name'] = players.name

    testing.to_csv('../resources/predictions/FOR_PREDS.csv', sep=',', encoding='utf-8')

get_forwards()