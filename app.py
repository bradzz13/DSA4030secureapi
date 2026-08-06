from extensions import db, jwt, bcrypt, limiter

import logging
import os
import sys
from pathlib import Path
from flask import Flask, jsonify



BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from routes.routes.customers import customers
from routes.routes.auth import auth

# CREATE FLASK APPLICATION
app = Flask(__name__)

app.register_blueprint(customers)


# DATABASE CONFIGURATION

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///secure_api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# JWT CONFIGURATION

app.config["JWT_SECRET_KEY"] = "1234"


# --------------------------------------------------
# INITIALIZE SECURITY COMPONENTS
# --------------------------------------------------

db.init_app(app)

jwt.init_app(app)

bcrypt.init_app(app)

limiter.init_app(app)


# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# --------------------------------------------------
# BASIC HOME ROUTE
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    logging.info("Home endpoint accessed")

    return jsonify({
        "message": "Secure Big Data API is running",
        "status": "success"
    })


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


# --------------------------------------------------
# RUN APPLICATION

app.register_blueprint(auth)


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )