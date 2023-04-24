
from flask import request, jsonify 
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from datetime import timedelta
from model.userModel import User
import controller.subscriptionController as subscriptionController

def create(request, bcrypt):
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        name = request.json.get('name')
        role = request.json.get('role')
        
        if len(password) < 3:
            raise ValueError("Password too short")
        
        existing_email = User.objects(email=email).first()
        if existing_email:
            raise ValueError("Email already in use")
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_customer = User(email=email, password=hashed_password, name=name, role=role)
        if role == "Customer":
            subscriptionController.setup_subscription(new_customer)
            new_customer.save()
        else:
            new_customer.save()
        return jsonify(new_customer), 200

    except ValueError as ve:
        response = jsonify({"error": str(ve)})
        response.status_code = 400
        return response
  
    
def login(request, bcrypt):
    try:
        
        email = request.json.get('email')
        password = request.json.get('password')
        selected_role = request.json.get('role')

        
        if len(password) < 3:
            raise ValueError("Password too short")
        
        user = User.objects(email=email).first()
        if not user:
            raise ValueError("Login Credentials does not exist")
        
        if user.role != selected_role:  
            raise ValueError("Invalid role for this email")
        
        if bcrypt.check_password_hash(user.password, password):
            # Set the expiration time to 30 minutes
            token = create_access_token(identity={"email": email, "role": user.role, "id": str(user.id), "name": user.name}, expires_delta=timedelta(minutes=30))
            refresh_token = create_refresh_token(identity={"email": email, "role": user.role, "id": str(user.id), "name": user.name})
            print("Generated access_token:", token)
            print("Generated refresh_token:", refresh_token)
            return jsonify({"token": token, "customer": user, "refresh_token": refresh_token}), 200
    
    except ValueError as ve:
        response = jsonify({"error": str(ve)})
        response.status_code = 400
        return response    

def refresh():
    current_user = get_jwt_identity()
    token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=15), fresh=False)
    print("Generated token in refresh():", token)
    return jsonify({"token": token}), 200


def reset(request, bcrypt):
    try:
        
        email = request.json.get('email')
        password = request.json.get('password')
        
        if len(password) < 3:
            raise ValueError("Password too short")
        
        existing_user = User.objects(email=email).first()
        if not existing_user:
            raise ValueError("Login Credentials does not exist")
        
        if not bcrypt.check_password_hash(existing_user.password, password):
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            existing_user.password = hashed_password
            existing_user.save()
            return jsonify({"message": "Password successfully changed!"}), 200
        else:
            raise ValueError("Error in changing password!")
    
    except ValueError as ve:
        response = jsonify({"error": str(ve)})
        response.status_code = 400
        return response       


