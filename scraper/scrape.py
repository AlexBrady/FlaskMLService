from __future__ import division
import requests
import json
from collections import namedtuple
import pandas as pd
from decimal import Decimal

a = 0
b = 1
c = 2
df_list = []

for i in range(1, 25):
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
result.drop_duplicates()

result.to_csv('./resources/17-18Ranks.csv', sep=',', encoding='utf-8')
