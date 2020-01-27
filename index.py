import os
import re
from flask import Flask
from flask import jsonify, abort, request, json
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, \
    jwt_refresh_token_required, create_refresh_token
from dbhelpers import DBHelpers
import datetime


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/v1/user/notes', methods=['GET'])
@jwt_required
def index():
    user = get_jwt_identity()
    user_notes = DBHelpers().list_user_notes(user['userid'])

    return jsonify(user_notes)


@app.route('/api/v1/user/<int:userID>/note/<slug>', methods=['GET'])
def show_note(userID, slug):
    note = DBHelpers().see_note(userID, slug)

    if note['public'] != 1:
        abort(404, description="Resource not found, or its private")

    return jsonify(note)


@app.route('/api/v1/user/login', methods=['POST'])
def login_user():
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = None

    user = DBHelpers().get_user(str(email))

    if user is None:
        result = jsonify({"error": "Потребителя не е намарен!"}), 401

    if user['verified'] == 1:
        if bcrypt.check_password_hash(user['password'], password):
            expires = datetime.timedelta(days=1)
            token = create_access_token(identity={"userid": user['id']},expires_delta=expires)
            refresh_token = create_refresh_token(identity={"userid": user['id']},expires_delta=expires)
            result = jsonify({"token": token, "refresh_token": refresh_token})
        else:
            result = jsonify({"error": "Невалидни данни"}), 401
    else:
        result = jsonify({"error": "Акаунта не е валидиран!"}), 403
    return result


@app.route('/api/v1/user/register', methods=['POST'])
def register_user():
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']

    create_user = DBHelpers().register_user(username, email, password)

    return create_user


@app.route('/api/v1/user/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_user_token():
    user = get_jwt_identity()
    expires = datetime.timedelta(days=1)
    token = create_access_token(identity={"userid": user['userid']},expires_delta=expires)
    refresh_token = create_refresh_token(identity={"userid": user['id']})

    return jsonify({'token': token,'refresh_token': refresh_token}), 200


@app.route('/api/v1/user')
@jwt_required
def user():
    user = get_jwt_identity()
    result = DBHelpers().get_user_data(user['userid'])

    return jsonify(result)

@app.route('/api/v1/user/stats')
@jwt_required
def user_stats():
    user = get_jwt_identity()
    user_stats = DBHelpers().get_user_statistics(user['userid'])

    return user_stats