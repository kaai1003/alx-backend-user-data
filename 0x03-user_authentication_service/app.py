#!/usr/bin/env python3
"""_summary_
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """GET welcome msg

    Returns:
        str: json payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """create user route"""
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    try:
        AUTH.register_user(user_email, user_pwd)
        return jsonify({"email": user_email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
