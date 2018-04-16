from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://monty:pass@46.101.50.178/FantasyPL'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.secret_key = 'brifbgib3huib4uifbg3bg4bfg3i4bfgoibg'


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.username

class Team(db.Model):
    __tablename__ = 'team'
    tid = db.Column(db.Integer)
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<team %r>' % self.uid


class MidPred(db.Model):
    __tablename__ = 'preds'
    player_id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Float, primary_key=True)
    name = db.Column(db.String(80))
    predicted = db.Column(db.Float)
    total_points = db.Column(db.Float)
    prediction_error = db.Column(db.Float)
    # __table_args__ = (
    #     PrimaryKeyConstraint('player_id', 'round'),
    #     {},
    # )

    def __init__(self, name, predicted):
        self.name = name
        self.predicted = predicted


class PlayerInfo(db.Model):
    __tablename__ = 'player_base'
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    web_name = db.Column(db.String(80))
    team_name = db.Column(db.String(80))
    pos = db.Column(db.String(24))
    minutes = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    goals_scored = db.Column(db.Integer)
    ict_index = db.Column(db.Float)
    bonus = db.Column(db.Integer)
    clean_sheets = db.Column(db.Integer)
    chance_of_playing_next_round = db.Column(db.Integer)
    now_cost = db.Column(db.Integer)
    code = db.Column(db.Integer)
    news = db.Column(db.Text)
    selected_by_percent = db.Column(db.Integer)
    total_points = db.Column(db.Integer)

    def __init__(self, player_id, first_name, web_name, team_name, pos, minutes,
                 assists, saves, goals_scored, ict_index, bonus,
                 clean_sheets, chance_of_playing_next_round, now_cost, code,
                 news, selected_by_percent, total_points):
        self.player_id = player_id
        self.first_name = first_name
        self.web_name = web_name
        self.team_name = team_name
        self.pos = pos
        self.minutes = minutes
        self.assists = assists
        self.saves = saves
        self.goals_scored = goals_scored
        self.ict_index = ict_index
        self.bonus = bonus
        self.clean_sheets = clean_sheets
        self.chance_of_playing_next_round = chance_of_playing_next_round
        self.now_cost = now_cost
        self.code = code
        self.news = news
        self.selected_by_percent = selected_by_percent
        self.total_points = total_points



