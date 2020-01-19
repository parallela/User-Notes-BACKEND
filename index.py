from flask import Flask
from flask import jsonify
from database import Database
import json

app = Flask(__name__)

@app.route('/api/user/<int:userID>/notes', methods=['GET'])
def index(userID):
    db = Database()
    user_notes = db.list_user_notes(userID)

    return jsonify(user_notes)
