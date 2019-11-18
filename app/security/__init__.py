from app.database import BaseMixin, db
from functools import wraps

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, create_access_token,
    get_jwt_claims
)
class TokenBlacklist(BaseMixin, db.Model):
    __tablename__ = 'tokenBlacklist'

    tokenID = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)

    def __init__(self, jti):
        self.jti = jti


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper