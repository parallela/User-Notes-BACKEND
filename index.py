from flask import Flask
from flask import jsonify
import json
from flask_cors import CORS
from dbhelpers import DBHelpers
#logging
from pprint import pprint

import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/v1/user/<int:userID>/notes', methods=['GET'])
def index(userID):
    user_notes = DBHelpers().list_user_notes(userID)
    
    return jsonify(user_notes)

# @app.route('/api/v1/show/note/<slug>', methods=['GET'])
# def show_note(slug):
#     note = DBHelpers().see_note(slug)
#     json_dict = json.loads(note)

#     for note in json_dict:
#         if(note['public'] == 0):
#             return jsonify(public=false)

#     return jsonify(note)
