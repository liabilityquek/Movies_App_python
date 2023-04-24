from flask import request, jsonify
from model.gameModel import Game
from model.userModel import User

def create_game(request, current_user_id):
    title = request.json.get('title')
    creator = request.json.get('creator')
    description = request.json.get('description')
    image_url = request.json.get('image_url')
    site = request.json.get('site')

    try:
        current_user = User.objects(id=current_user_id).first()

        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404

        current_game = Game.objects(title=title).first()
        if current_game is not None:
            error_message = f"{title} has already been added"
            return jsonify({"error": error_message}), 400
        else:
            new_game = Game(title=title, creator=creator, description=description, image_url=image_url, site=site)
            new_game.save()

        print("new_game:", new_game)
        return jsonify(new_game), 200

    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400


def show_all_games(current_user_id):
    try:
        current_user = User.objects(id=current_user_id).first()
        
        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404
        else:
            games = Game.objects()
            
            if not games:
                return jsonify({"message": "Nothing to show..."}), 200
            else:
                return jsonify({"games": games}), 200
                 
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400
    
def edit_games(current_user_id, game_id, updated_title=None, updated_creator=None, updated_desc=None, update_image=None, update_site=None):
    
    try:
        current_user = User.objects(id=current_user_id).first()
        
        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404
        else:
            current_game = Game.objects(id=game_id).first()
            
            if not current_game:
                return jsonify({"message": "Nothing to edit..."}), 200
            else:
                if updated_title is not None:
                    current_game.title = updated_title
                if updated_creator is not None:
                    current_game.creator = updated_creator
                if updated_desc is not None:
                    current_game.description = updated_desc
                if update_image is not None:
                    current_game.image_url = update_image
                if update_site is not None:
                    current_game.site = update_site
                    
                
                current_game.save()
                
                return jsonify({"message": "Game updated successfully"}), 200
                 
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400    
    
def delete_game(current_user_id, title):
   
    try:
        current_user = User.objects(id=current_user_id).first()

        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404
        else:
            game_to_remove = Game.objects(title=title).first()

            if not game_to_remove:
                error_message = f"{title} is not in your game list"
                return jsonify({"error": error_message}), 404
            else:
                game_to_remove.delete()
                return jsonify({"message": f"{title} has been removed from your game list"}), 200

    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400
    
def add_likes(current_user_id, game_id):
    try:
        
        current_user = User.objects(id=current_user_id).first()
        game = Game.objects(id=game_id).first()
        
        if current_user is None or game is None:
            return jsonify({"error": "User or game not found"}), 404
        
        if current_user not in game.likes:
            game.likes.append(current_user)
            game.save()
            return jsonify({"message": "Like added successfully"}), 200
        else:
            return jsonify({"message": "You have already liked this game"}), 400
    
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400
    
def remove_likes(current_user_id, game_id):
    try:
        current_user = User.objects(id=current_user_id).first()
        game = Game.objects(id=game_id).first()
        
        if current_user is None or game is None:
            return jsonify({"error": "User or game not found"}), 404
        
        if current_user in game.likes:
            game.likes.remove(current_user)
            game.save()
            return jsonify({"message": "Like removed successfully"}), 200
        
        else:
            return jsonify({"message": "User has not liked this game"}), 400
    
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400       
                   
def get_user_id_in_game(game_id, current_user_id):
    game = Game.objects(id=game_id).first()
    print(f"Game ID: {game_id}")
    
    if game is None:
        return jsonify({"error": "User have not liked this game yet."}), 404
    
    else:
        user_liked = any(str(user.id) == current_user_id for user in game.likes)
        game_data = {
            "game_id": str(game.id),
            "user_liked": user_liked
        }
    
    return jsonify(game_data), 200

def single_game(current_user_id, game_id):
    try:
        current_user = User.objects(id=current_user_id).first()
        game = Game.objects(id=game_id).first()
        
        if current_user is None or game is None:
            return {"error": "User or game not found"}, 404
        else:
            return jsonify(game)
    
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {"error": error_message}, 400
   

