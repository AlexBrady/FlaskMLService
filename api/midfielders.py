# from api.sdg_predict import get_midfielder, get_defender, get_forward, get_goalkeeper
from flask import session, request, jsonify
from flask_login import current_user
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict
from .models import User, db, app, MidPred, PlayerInfo, Team
from .schemas import mid_schema, player_schema, user_schema, team_schema



@app.route("/Register/", methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = User(username=username, email=email, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        status = 'Success'
    except:
        status = 'already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route("/AuthenticateUser/", methods=['GET', 'POST'])
def authenticateUser():
    try:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['pasword'] = password
            status = True
            return jsonify({'result': status})
        else:
            status = False
            return jsonify({'result': status})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})


@app.route("/getUser/", methods=['GET', 'POST'])
def get_user():
    try:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['logged_in'] = True
            session['username'] = username
            session['pasword'] = password
            return user_schema.jsonify(user)
        else:
            status = False
            return jsonify({'result': status})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/status/')
def status():
    if session.get('username') is 'beaner':
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})


@app.route('/saveTeam/', methods=['POST'])
def save_team():
    tid = request.form['tid']
    pid = request.form['pid']
    uid = request.form['uid']
    team = Team(tid=tid, pid=pid, uid=uid)
    try:
        db.session.add(team)
        db.session.commit()
        status = 'Success'
    except Exception as e:
        status = 'error'
        print(e)
    db.session.close()
    return jsonify({'result': status})


@app.route('/loadTeam/', methods=['POST'])
def load_team():
    tid = request.form['tid']
    uid = request.form['uid']
    team = Team.query.filter_by(tid=tid, uid=uid).all()
    if team:
        return team_schema.jsonify(team)
    else:
        status = False
        return jsonify({'result': status})


@app.route("/get_player_details/", methods=['GET'])
def get_all_players():
    player_list = PlayerInfo.query.all()

    return player_schema.jsonify(player_list, many=True)


@app.route("/get_single_player/<id>")
def get_player(id: int):
    play = PlayerInfo.query.get(id)

    return player_schema.jsonify(play)

@app.route("/preds/<id>", methods=['GET'])
def get_players(id: int):
    pred = MidPred.query.filter_by(player_id=id, round=35)

    return mid_schema.jsonify(pred)


@app.route("/all_preds/<id>", methods=['GET'])
def get_mid(id: int):
    pred = MidPred.query.get(id)

    return mid_schema.jsonify(pred)

@app.route('/past_preds/<id>', methods=['GET'])
def get_past_preds(id: int):
    preds = MidPred.query.filter_by(player_id=id).all()
    
    return mid_schema.jsonify(preds, many=True)

# @app.route("/defender/<name>", methods=['GET'])
# def get_def(name: str):
#     player = get_defender(name)
#
#     return player.to_json()
#
# @app.route("/forward/<name>", methods=['GET'])
# def get_forw(name: str):
#     player = get_forward(name)
#
#     return player.to_json()
#
# @app.route("/goalkeeper/<name>", methods=['GET'])
# def get_goalk(name: str):
#     player = get_goalkeeper(name)
#
#     return player.to_json()

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
