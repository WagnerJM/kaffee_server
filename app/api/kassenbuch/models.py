from app.database import db, BaseMixin
from app.serializer import ma 
#from app.api.user.models import User


class Kassenbuch(db.Model, BaseMixin):
    __tablename__ = "kassenbuch"

    #user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    coffee_count = db.Column(db.Integer)
    aktueller_kaffee_preis = db.Column(db.Float)
    betrag = db.Column(db.Float)
    bezahlt = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, coffee_count, aktueller_kaffee_preis, betrag):
        self.user_id = user_id
        self.coffee_count = coffee_count
        self.aktueller_kaffee_preis = aktueller_kaffee_preis
        self.betrag = betrag
    

class KassenbuchSchema(ma.ModelSchema):
    class Meta:
        model = Kassenbuch
        fields = (
            "coffee_count",
            "aktueller_kaffee_preis",
            "betrag",
            "bezahlt"
        )
    
