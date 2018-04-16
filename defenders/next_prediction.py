import math
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn import svm

data = pd.read_csv('../resources/newMERGED.csv', sep=',', encoding='utf-8', index_col=0)
model = data[['player_id', 'name', 'season', 'pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
              'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points',
              'long_form', 'ict_form']]

DefenderModal = model.loc[model['pos'] == 'Defender']
DefenderModal.drop('pos', axis=1, inplace=True)
DefenderModal.sort_values(['season', 'round'], ascending=True, inplace=True)
DefenderModal.to_csv('../temp/DEFENDERS.csv', sep=',', encoding='utf-8')
players = DefenderModal[5732:]

keys = DefenderModal['round']
values = pd.cut(DefenderModal['round'], 3, labels=[1, 2, 3])
dictionary = dict(zip(keys, values))
DefenderModal['round'] = values

X = DefenderModal.drop(['total_points', 'season', 'long_form', 'team_pot', 'opp_concede_pot', 'player_id', 'name'], axis=1)
y = DefenderModal[['total_points']]

X_train = X[:5731]
X_test = X[5732:]
y_train = y[:5731]
y_test = y[5732:]

regression_model = LinearRegression()
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

testing.to_csv('../resources/predictions/defender_preds.csv', sep=',', encoding='utf-8')
