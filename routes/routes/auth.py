from flask import Blueprint, request, jsonify

from flask_jwt_extended import create_access_token

from extensions import db, bcrypt, limiter

from models import User

import logging



auth = Blueprint(
    "auth",
    __name__
)


# LOGIN ENDPOINT

@auth.route(
    "/login",
    methods=["POST"]
)
@limiter.limit("5 per minute")
def login():

    # ----------------------------------------
    # GET JSON DATA
    # ----------------------------------------

    data = request.get_json()


    # ----------------------------------------
    # VALIDATE INPUT
    # ----------------------------------------

    if not data:

        return jsonify({
            "message": "Request must contain JSON data"
        }), 400


    username = data.get("username")

    password = data.get("password")


    if not username or not password:

        logging.warning(
            "Login attempt missing username or password"
        )

        return jsonify({
            "message": "Username and password are required"
        }), 400


    # ----------------------------------------
    # FIND USER
    # ----------------------------------------

    user = User.query.filter_by(
        username=username
    ).first()


    # ----------------------------------------
    # CHECK PASSWORD
    # ----------------------------------------

    if not user or not bcrypt.check_password_hash(
        user.password_hash,
        password
    ):

        logging.warning(
            f"Failed login attempt for username: {username}"
        )

        return jsonify({
            "message": "Invalid username or password"
        }), 401


    # ----------------------------------------
    # CREATE JWT TOKEN
    # ----------------------------------------

    access_token = create_access_token(

        identity=str(user.id),

        additional_claims={
            "username": user.username,
            "role": user.role
        }

    )


    # ----------------------------------------
    # LOG SUCCESSFUL LOGIN
    # ----------------------------------------

    logging.info(
        f"Successful login: "
        f"user={user.username}, "
        f"role={user.role}"
    )


    return jsonify({

        "message": "Login successful",

        "access_token": access_token,

        "user": {

            "username": user.username,

            "role": user.role

        }

    }), 200