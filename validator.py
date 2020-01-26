import re
from flask import jsonify

class Validator:
    def validate_register_credentials(self, **data):
        message = jsonify({"error": "Невалидни данни за регистрация"}), 401

        if re.match("^[a-zA-Z0-9_.-]+$", data['username']) and len(data['password']) > 7:
            result = True
        else:
            result = message

        return result






