from flask import request, jsonify
from model.favouriteModel import Favourite, User

def create_favourite(request, current_user_id):
    # print(f"current_user_id: {current_user_id}")

    title = request.json.get('title')
    year = request.json.get('year')
    rating = request.json.get('rating')
    description = request.json.get('description')
    image_url = request.json.get('image_url')

    try:
        current_user = User.objects(id=current_user_id).first()

        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404

        current_title = Favourite.objects(name=current_user, title=title).first()
        if current_title is not None:
            error_message = f"{title} has already been added to your favourites"
            return jsonify({"error": error_message}), 400
        else:
            new_favourite = Favourite(name=current_user, title=title, year=year, rating=rating, description=description, image_url=image_url)
            new_favourite.save()

        print("updated_favourite:", new_favourite)
        return jsonify(new_favourite), 200

    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400


def show_favourite(request, current_user_id):
    # print(f"current_user_id: {current_user_id}")
    
    try:
        current_user = User.objects(id=current_user_id).first()
        
        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404
        else:
            favourites = Favourite.objects(name=current_user)
            
            if not favourites:
                return jsonify({"message": "Nothing to show..."}), 200
            else:
                return jsonify({"favourites": favourites}), 200

            
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400
    
def show_single_movie_favourite(request, current_user_id, title):
    
    try:
        current_user = User.objects(id=current_user_id).first()
        
        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404
        else:
            favourites = Favourite.objects(name=current_user, title=title).first()
            
            if not favourites:
                return jsonify({"message": "Nothing to show..."}), 200
            else:
                return jsonify({"favourites": favourites}), 200

            
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400    

def delete_favourite(current_user_id, title):
    # print(f"current_user_id: {current_user_id}")
    
    try:
        current_user = User.objects(id=current_user_id).first()

        if current_user is None:
            error_message = f"User with ID {current_user_id} does not exist."
            print(error_message)
            return jsonify({"error": error_message}), 404
        else:
            favourite_to_remove = Favourite.objects(name=current_user, title=title).first()

            if not favourite_to_remove:
                error_message = f"{title} is not in your favourites"
                return jsonify({"error": error_message}), 404
            else:
                favourite_to_remove.delete()
                return jsonify({"message": f"{title} has been removed from your favourites"}), 200

    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400



