import math
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn import svm

data = pd.read_csv('../resources/newMERGED.csv', sep=',', encoding='utf-8', index_col=0)
model = data[['pos', 'round', 'team_rank', 'opponent_team_rank', 'team_pot', 'opp_pot',
              'concede_pot', 'opp_concede_pot', 'prev_points', 'form_points', 'total_points',
              'long_form', 'ict_form']]

ForwardModal = model.loc[model['pos'] == 'Forward']
ForwardModal.drop('pos', axis=1, inplace=True)

keys = ForwardModal['round']
values = pd.cut(ForwardModal['round'], 3, labels=[1, 2, 3])
dictionary = dict(zip(keys, values))
ForwardModal['round'] = values

X = ForwardModal.drop(['total_points', 'concede_pot', 'opp_pot'], axis=1)
y = ForwardModal[['total_points']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=None)
regression_model = SGDRegressor()
regression_model.fit(X_train, y_train)
y_pred = regression_model.predict(X_test)
testing = pd.concat([X_test, y_test], 1)
testing['Predicted'] = np.round(y_pred, 1)
testing['Prediction_Error'] = testing['total_points'] - testing['Predicted']
testing['Prediction_Error'] = testing['Prediction_Error'].abs()
print('Avg Error:')
print(testing.Prediction_Error.mean())
print('Modal score:')
print(regression_model.score(X_test, y_test))
# linreg = LinearRegression()
# scores = cross_val_score(linreg, X, y, cv=10, scoring='neg_mean_squared_error')
# scores = -scores
# scores = np.sqrt(scores)
# print(scores.mean())

testing.to_csv('../resources/FOR_SDG.csv', sep=',', encoding='utf-8')
good = testing[testing['Prediction_Error'] < 1.5]
bad = testing[testing['Prediction_Error'] >= 1.5]

print('Percentage of close predictions: ')
(len(good.index) / len(testing.index) * 100)