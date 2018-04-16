import math
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn import svm

data = pd.read_csv('../resources/newMERGED.csv', sep=',', encoding='utf-8', index_col=0)
model = data[['player_id', 'name', 'season', 'pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
              'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points', 'save_form',
              'long_form', 'ict_form']]

GoalkeeperModal = model.loc[model['pos'] == 'Goalkeeper']
GoalkeeperModal.drop('pos', axis=1, inplace=True)
GoalkeeperModal.sort_values(['season', 'round'], ascending=True, inplace=True)
# GoalkeeperModal.to_csv('../temp/DEFENDERS.csv', sep=',', encoding='utf-8')
players = GoalkeeperModal[5732:]

keys = GoalkeeperModal['round']
values = pd.cut(GoalkeeperModal['round'], 3, labels=[1, 2, 3])
dictionary = dict(zip(keys, values))
GoalkeeperModal['round'] = values

X = GoalkeeperModal.drop(['total_points', 'season', 'long_form', 'team_pot', 'opp_concede_pot', 'player_id', 'name'], axis=1)
y = GoalkeeperModal[['total_points']]

X_train = X[:5731]
X_test = X[5732:]
y_train = y[:5731]
y_test = y[5732:]

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

print('Avg Error:')
print(testing.Prediction_Error.mean())
print('Modal score:')
print(regression_model.score(X_test, y_test))

testing.to_csv('../resources/predictions/GOALK_sdg_predictions.csv', sep=',', encoding='utf-8')
