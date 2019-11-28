import os
from flask import Flask 
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate 

from app.config import app_config

from app.database import db
from app.serializer import ma
from app.cache import redis_client
from app.security import TokenBlacklist

def create_app():

	app = Flask(__name__)
	api = Api(app)
	config_name = os.getenv("FLASK_ENV")
	cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080", "http://localhost:8080/" ]}})
	app.config['CORS_HEADERS'] = 'Content-Type'
	app.config.from_object(app_config[config_name])
	jwt = JWTManager(app)

	@jwt.user_claims_loader
	def add_claims_to_jwt(identity):
		from app.api.user.models import User
		user = User.find_by_id(identity)

		if user.is_admin:
			return {'roles': "admin"}
		return {'roles': "user"}

	@jwt.token_in_blacklist_loader
	def check_if_token_in_blacklist(decrypted_token):
		from app.security import TokenBlacklist

		return decrypted_token['jti'] in TokenBlacklist.get_all()

	@jwt.expired_token_loader
	def expired_token_callback():

		return jsonify({
                    'description': 'The token has expired',
                    'error': 'token_expired'
		}), 401

	@jwt.invalid_token_loader
	def invalid_token_callback(error):
		return jsonify({
                    'description': 'Signature verification failed.',
                    'error': 'invalid_token'
		}), 401

	@jwt.unauthorized_loader
	def missing_token_callback(error):
		return jsonify({
                    'description': 'Request does not contain an access token.',
                    'error': 'authorization_required'
		}), 401

	@jwt.needs_fresh_token_loader
	def token_not_fresh_callback():
		return jsonify({
                    'description': 'The token is not fresh.',
                    'error': 'fresh_token_required'
                }), 401

	@jwt.revoked_token_loader
	def revoked_token_callback():
		return jsonify({
                    'description': 'The token has been revoked.',
                    'error': 'token_revoked'
                }), 401

	##import area
	from app.api.user.resources import (
		UserApi, 
		UserRegisterApi, 
		UserLoginApi, 
		UserLogoutApi, 
		AdminUsersApi,
		UserCoffeeApi
	) 
	api.add_resource(UserRegisterApi, "/api/v1/register")
	api.add_resource(UserLoginApi, "/api/v1/login")
	api.add_resource(UserLogoutApi, "/api/v1/logout")
	api.add_resource(UserApi, "/api/v1/user")
	api.add_resource(AdminUsersApi, "/api/v1/admin/user")
	api.add_resource(UserCoffeeApi, "/api/v1/user/coffee")
	
	from app.api.system.resources import SystemSettingUpdateApi, SystemSettingApi, RechnungsApi
	api.add_resource(SystemSettingApi, "/api/v1/admin/settings")
	api.add_resource(SystemSettingUpdateApi, "/api/v1/admin/setting")
	api.add_resource(RechnungsApi, "/api/v1/admin/rechnungslauf")

	"""from app.api.kassenbuch.resources import KassenbuchListApi, KassenbuchApi
	api.add_resource(KassenbuchListApi, "/api/v1/kassenbuch")
	api.add_resource(KassenbuchApi, "/api/v1/kassenbuch/<int:id>")
	"""
	redis_client.init_app(app)
	db.init_app(app)
	migrate = Migrate(app, db)
	ma.init_app(app)

	return app