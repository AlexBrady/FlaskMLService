from marshmallow_sqlalchemy import ModelSchema
from .models import User, MidPred, PlayerInfo, app, db, ma, Team

class MidPredSchema(ma.ModelSchema):
    class Meta:
        model = MidPred

class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = PlayerInfo

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class TeamSchema(ma.ModelSchema):
    class Meta:
        model = Team

mid_schema = MidPredSchema(strict=True)
player_schema = PlayerSchema()
user_schema = UserSchema()
team_schema = TeamSchema(many=True)
