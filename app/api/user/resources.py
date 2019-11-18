from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt

from app.security import TokenBlacklist
from app.api.user.models import User, UserSchema
import datetime
from app.database import db
from app.security import admin_required

class UserRegisterApi(Resource):
    def post(self):
        response = {}
        data = request.get_json()
        
        if User.find_by_username(data['username']):
            response['status'] = "ERROR"
            response['message'] = "Username ist bereits vergeben."
            return response, 500
        
        user = User(**data)
        user.save()
        response['status'] = "OK"
        response['message'] = "User wurde erfolgreich angelegt."
        return response, 201


class UserLoginApi(Resource):
    def post(self):
        response = {}
        data = request.get_json()
        user = User.find_by_username(data['username'])
        if user and user.check_pw(password=data['password'], hashed_pw=user._password):
            token = create_access_token(identity=str(user.id),
                                        fresh=True,
                                        expires_delta=datetime.timedelta(
                minutes=60
            )
            )
            response['token'] = token
            response['username'] = user.username
            response['status'] = "OK"
            response['message'] = "User wurde angemeldet"

            return response, 200
        else:
            response['status'] = "ERROR"
            response['message'] = "Username und/oder Passwort sind falsch"
            return response, 403


class UserLogoutApi(Resource):
    @jwt_required
    def post(self):
        response = {}
        
        response['status'] = "OK"
        response["message"] = "Erfolgreich ausgeloggt"
        return response, 200


class UserApi(Resource):
    @jwt_required
    def get(self):
        user = User.find_by_id(get_jwt_identity())
        schema = UserSchema()

        response = {
            "status": "OK",
            "user": schema.dump(user).data
        }
        return response, 200
    
    @jwt_required
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id)
        user.update(request.json)
        db.session.commit()

        user = User.find_by_id(get_jwt_identity())
        schema = UserSchema()

        response = {
            "status": "OK",
            "user": schema.dump(user).data
        }
        return response, 200

class AdminUsersApi(Resource):
    
    @admin_required
    def get(self):
        #get all users for admin
        schema = UserSchema(many=True)
        users = User.get_all()
        return schema.dump(users).data, 200
    
    
    @admin_required
    def post(self):
        pass

class UserCoffeeApi(Resource):
    
    def get(self):
        users = User.get_all()
        user_list = []
        for user in users:
            obj = {
                "username": user.username,
                "coffeeCount": user.coffee_count
            }
            user_list.append(obj)
        
        return user_list, 200