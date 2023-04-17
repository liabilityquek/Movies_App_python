from flask import request, jsonify 
from flask_jwt_extended import create_access_token
from datetime import timedelta
from model.userModel import User

def create(request, bcrypt):
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')
    role = request.json.get('option')
    
    if len(password) < 3:
        return jsonify({"message": "Password too short"}), 400
    
    existing_email = User.objects(email=email).first()
    if existing_email:
        return jsonify({"message": "Email already in use"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_customer = User(email=email, password=hashed_password, name=name, role=role)
    new_customer.save()
    return jsonify(new_customer), 201


def login(request, bcrypt):
    email = request.json.get('email')
    password = request.json.get('password')
    selected_role = request.json.get('role')

    
    if len(password) < 3:
        return jsonify({"message": "Password too short"}), 400
    
    user = User.objects(email=email).first()
    if not user:
        return jsonify({"message": "Login Credentials does not exist!"}), 400
    
    if user.role != selected_role:  
        return jsonify({"message": "Invalid role for this email"}), 400
    
    if bcrypt.check_password_hash(user.password, password):
        # Set the expiration time to 30 minutes
        token = create_access_token(identity={"email": email, "role": user.role, "id": str(user.id), "name": user.name}, expires_delta=timedelta(minutes=30))
        return jsonify({"token": token, "customer": user}), 200


def reset(request, bcrypt):
    email = request.json.get('email')
    password = request.json.get('password')
    
    if len(password) < 3:
        return jsonify({"message": "Password too short"}), 400
    
    existing_user = User.objects(email=email).first()
    if not existing_user:
        return jsonify({"message": "Invalid Credentials!"}), 400
    
    if not bcrypt.check_password_hash(existing_user.password, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user.password = hashed_password
        existing_user.save()
        return jsonify({"message": "Password successfully changed!"}), 200
    else:
        return jsonify({"message": "Error in changing password!"}), 401

