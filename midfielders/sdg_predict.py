import math
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn import svm

def player_prediction(name):

    data = pd.read_csv('../resources/newMERGED.csv', sep=',', encoding='utf-8', index_col=0)
    model = data[['player_id', 'name', 'season', 'pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
                  'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points',
                  'long_form', 'ict_form']]

    MidfielderModal = model.loc[model['pos'] == 'Midfielder']
    MidfielderModal.drop('pos', axis=1, inplace=True)
    MidfielderModal.sort_values(['season', 'round'], ascending=True, inplace=True)
    # MidfielderModal.to_csv('../temp/MIDFIELDERS.csv', sep=',', encoding='utf-8')
    players = MidfielderModal[7959:]

    keys = MidfielderModal['round']
    values = pd.cut(MidfielderModal['round'], 3, labels=[1, 2, 3])
    dictionary = dict(zip(keys, values))
    MidfielderModal['round'] = values

    X = MidfielderModal.drop(['total_points', 'season', 'player_id', 'name'], axis=1)
    y = MidfielderModal[['total_points']]

    X_train = X[:7958]
    X_test = X[7959:]
    y_train = y[:7958]
    y_test = y[7959:]

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

    print(testing[testing['name'] == name])
    # testing.to_csv('../resources/predictions/SGDmidfielder_preds.csv', sep=',', encoding='utf-8')
