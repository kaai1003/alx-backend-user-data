#!/usr/bin/env python3
""" Module of Session Auth
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def post_login():
    """login route method"""
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    search_users = User.search({'email': email})
    if not search_users or search_users == []:
        return jsonify(
            {"error": "no user found for this email"}
            ), 404
    for user in search_users:
        if user.is_valid_password():
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(os.getenv('SESSION_NAME'),
                                sess_id)
            return response
        return jsonify({"error": "wrong password"}), 401
