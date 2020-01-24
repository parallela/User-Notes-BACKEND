from flask import Flask
from flask import jsonify
from flask_cors import CORS
from dbhelpers import DBHelpers

import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/v1/user/<int:userID>/notes', methods=['GET'])
def index(userID):
    user_notes = DBHelpers().list_user_notes(userID)

    return jsonify(user_notes)
