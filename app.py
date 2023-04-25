from flask import Flask, request, jsonify, send_from_directory
import controller.favouriteController as favouriteController
import controller.historyController as historyController
import controller.loginController as loginController
import controller.authController as authController
import controller.gameController as gameController
import controller.subscriptionController as subscriptionController
from flask.helpers import send_from_directory
from flask_bcrypt import Bcrypt
from config.database import init_database
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv
import os
load_dotenv()

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

@app.route("/login", methods=["POST"])
def user_login():
    try:
        response = loginController.login(request, bcrypt)
        return response 
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route("/create", methods=["POST"])
def user_create():
    try:
        response = loginController.create(request, bcrypt)
        return response
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route("/reset", methods=["POST"])
def user_reset():
    try:
        response = loginController.reset(request, bcrypt)
        return response
    except ValueError as e:
        return jsonify({"message": str(e)}), 400   

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

@app.route("/showgames/<current_user_id>", methods=["GET"])
@authController.auth
@authController.require_role(["Customer", "Admin"])
def show_games(current_user_id):
    return gameController.show_all_games(current_user_id)

@app.route("/showsinglegame/<current_user_id>/<game_id>", methods=["GET"])
@authController.auth
@authController.require_role(["Admin"])
def show_single_game(current_user_id, game_id): 
    return gameController.single_game(current_user_id, game_id)


@app.route("/deletegame/<current_user_id>/<title>", methods=["DELETE"])
@authController.auth
@authController.require_role(["Admin"])
def remove_game(current_user_id, title):
    return gameController.delete_game(current_user_id, title)

@app.route("/creategame/<current_user_id>", methods=["POST"])
@authController.auth
@authController.require_role(["Admin"])
def new_game(current_user_id):
    return gameController.create_game(request, current_user_id)

@app.route("/updategame/<current_user_id>/<id>", methods=["PUT"])
@authController.auth
@authController.require_role(["Admin"])
def amend_game(current_user_id, id):
    updated_title = request.json.get("updated_title", None)
    updated_creator = request.json.get("updated_creator", None)
    updated_desc = request.json.get("updated_desc", None)
    update_image = request.json.get("update_image", None)
    update_site = request.json.get("update_site", None)

    return gameController.edit_games(
        current_user_id,
        id,
        updated_title=updated_title,
        updated_creator=updated_creator,
        updated_desc=updated_desc,
        update_image=update_image,
        update_site=update_site,
    )

@app.route("/newlikes/<current_user_id>/<game_id>", methods=["POST"])
@authController.auth
@authController.require_role(["Customer"])
def new_like(current_user_id, game_id):
    return gameController.add_likes(current_user_id, game_id)

@app.route("/deletelikes/<current_user_id>/<game_id>", methods=["DELETE"])
@authController.auth
@authController.require_role(["Customer"])
def del_like(current_user_id, game_id):
    return gameController.remove_likes(current_user_id, game_id)

@app.route("/checklikes/<game_id>/<current_user_id>", methods=["GET"])
@authController.auth
@authController.require_role(["Customer"])
def check_like(game_id, current_user_id):
    return gameController.get_user_id_in_game(game_id, current_user_id)

@app.route("/cancelsubscription/<user_id>", methods=["POST"])
@authController.auth
@authController.require_role(["Customer"])
def handle_cancel_subscription(user_id):
    try:
        subscriptionController.cancel_subscription(user_id)
        return jsonify({"message": "Subscription cancelled successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route("/amendsubscription/<user_id>", methods=["POST"])
@authController.auth
@authController.require_role(["Customer"])
def handle_amend_subscription(user_id):
    new_plan = request.json.get('plan')
    try:
        message = subscriptionController.amend_subscription_plan(user_id, new_plan)
        return jsonify({"message": message}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
@app.route("/reinstatesubscription/<user_id>", methods=["POST"])
@authController.auth
@authController.require_role(["Customer"])
def handle_reinstate_subscription(user_id):
    try:
        message = subscriptionController.reinstate_subscription(user_id)
        return jsonify({"message": message}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route("/getsubscriptiondetails/<user_id>", methods=["GET"])
@authController.auth
@authController.require_role(["Customer"])
def handle_get_subscription_details(user_id):
    try:
        message = subscriptionController.get_subscription_details(user_id)
        return jsonify({"message": message}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    return loginController.refresh()

if __name__ == "__main__":
    app.run()