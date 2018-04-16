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
              'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points', 'save_form',
              'long_form', 'ict_form']]

GoalkeeperModal = model.loc[model['pos'] == 'Goalkeeper']
GoalkeeperModal.drop('pos', axis=1, inplace=True)
GoalkeeperModal.sort_values(['season', 'round'], ascending=True, inplace=True)
GoalkeeperModal.to_csv('../temp/GOALKEEPERS.csv', sep=',', encoding='utf-8')
players = GoalkeeperModal[1294:]

keys = GoalkeeperModal['round']
values = pd.cut(GoalkeeperModal['round'], 3, labels=[1, 2, 3])
dictionary = dict(zip(keys, values))
GoalkeeperModal['round'] = values

X = GoalkeeperModal.drop(['total_points', 'season', 'ict_form', 'long_form', 'opp_concede_pot', 'player_id', 'name'], axis=1)
y = GoalkeeperModal[['total_points']]

X_train = X[:1293]
X_test = X[1294:]
y_train = y[:1293]
y_test = y[1294:]

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

testing.to_csv('../resources/predictions/goalkeeper_preds.csv', sep=',', encoding='utf-8')
