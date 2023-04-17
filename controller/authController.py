from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.userModel import User

def auth(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        email = identity['email']
        role = identity['role']
        user = User.objects(email=email, role=role).first()

        if user:
            request.user = user
            return fn(*args, **kwargs)
        else:
            return jsonify({"message": "Forbidden"}), 403

    return wrapper

def require_role(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not request.user or request.user.role not in roles:
                return jsonify({"message": "Forbidden"}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper