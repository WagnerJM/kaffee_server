"""from flask import request
from flask_restful import Resource

from app.security import admin_required
from app.database import db
from app.api.user.models import User, UserSchema
from app.api.kassenbuch.models import Kassenbuch, KassenbuchSchema

class KassenbuchListApi(Resource):
    @admin_required
    def get(self):
        response = {}
        kassenbuch_list = Kassenbuch.get_all()
        schema = KassenbuchSchema(many=True)
        response["kassenbuch_liste"] = schema.dump(kassenbuch_list).data
        return response, 200


class KassenbuchApi(Resource):
    @admin_required
    def put(self, eintrag_id):

        kassenbuch_eintrag = Kassenbuch.query.filter_by(id=eintrag_id)
        kassenbuch_eintrag.update(request.json)
        db.session.commit()
        kassenbuch_list = Kassenbuch.get_all()
        schema = KassenbuchSchema(many=True)
        response["kassenbuch_liste"] = schema.dump(kassenbuch_list).data
        return response, 200
    

"""