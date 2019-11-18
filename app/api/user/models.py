import bcrypt
from app.database import db, BaseMixin
from app.serializer import ma
#from app.api.kassenbuch.models import Kassenbuch, KassenbuchSchema
from marshmallow.fields import Nested 

class User(db.Model, BaseMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(60), nullable=False)
    _password = db.Column(db.LargeBinary(60))
    vorname = db.Column(db.String(60))
    nachname = db.Column(db.String(60))
    is_admin = db.Column(db.Boolean)
    email = db.Column(db.String(60))
    key_ID = db.Column(db.String(60))
    coffee_count = db.Column(db.Integer, default=0)
    #kassenbuch_eintraege = db.relationship("Kassenbuch", backref="User", lazy=False)

    def __init__(self, username, password, email):
        self.username = username
        self._password = self.hash_pw(password.encode('utf-8'))
        self.email = email


    def hash_pw(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt(12))
    
    def check_pw(self, password, hashed_pw):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class UserSchema(ma.ModelSchema):
   #kassenbuch_eintraege = Nested(KassenbuchSchema, many=True)
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "is_admin", 
            "email",
            "key_ID",
            "coffee_count"
        )
    