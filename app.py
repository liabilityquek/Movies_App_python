from flask import Flask, request, jsonify, send_from_directory
import controller.favouriteController as favouriteController
import controller.historyController as historyController
import controller.loginController as loginController
import controller.authController as authController
from flask.helpers import send_from_directory
from flask_bcrypt import Bcrypt
from config.database import init_database
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import unset_jwt_cookies
import os

app = Flask(__name__, static_folder="dist/assets")
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, supports_credentials=True)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
init_database(app)

@app.route("/")
def home():
    return send_from_directory("dist", "index.html")


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/login", methods=["POST"])
def user_login():
   return loginController.login(request, bcrypt)

@app.route("/create", methods=["POST"])
def user_create():
    return loginController.create(request,bcrypt)

@app.route("/reset", methods=["POST"])
def user_reset():
    return loginController.reset(request,bcrypt)

@app.route("/history", methods=["POST"])
@authController.auth
@authController.require_role(["Customer"])
def new_history():
    return historyController.create_history(request)

@app.route("/showhistory", methods=["GET"])
@authController.auth
@authController.require_role(["Customer"])
def history():
    return historyController.show_history(request)

@app.route("/favourite/<current_user_id>", methods=["POST"])
@authController.auth
@authController.require_role(["Customer"])
def new_favourite(current_user_id):
    return favouriteController.create_favourite(request, current_user_id)

@app.route("/showfavourite/<current_user_id>", methods=["GET"])
@authController.auth
@authController.require_role(["Customer"])
def favourite(current_user_id):
    return favouriteController.show_favourite(request, current_user_id)

@app.route("/showsinglefavourite/<current_user_id>/<title>", methods=["GET"])

@authController.auth
@authController.require_role(["Customer"])
def single_favourite(current_user_id, title):
    return favouriteController.show_single_movie_favourite(request, current_user_id, title)

@app.route("/deletefavourite/<current_user_id>/<title>", methods=["DELETE"])
@authController.auth
@authController.require_role(["Customer"])
def del_favourite(current_user_id, title):
    return favouriteController.delete_favourite(current_user_id, title)

if __name__ == "__main__":
    app.run()