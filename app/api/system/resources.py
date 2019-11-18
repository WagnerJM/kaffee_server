from flask import request
from flask_restful import Resource

from app.security import admin_required
from app.database import db
from app.api.system.models import SystemSetting, SystemSettingSchema

class SystemSettingApi(Resource):
    
    @admin_required
    def get(self):
        response = {}
        settings = SystemSetting.get_settings()
        schema = SystemSettingSchema()
        response['status'] = "OK"
        response['system_settings'] = schema.dump(settings).data

        return response, 200

class SystemSettingUpdateApi(Resource):

    @admin_required
    def put(self):
        response = {}
        schema = SystemSettingSchema()
        

        
        settings = SystemSetting.query.filter_by(id=1)
        settings.update(request.json)
        db.session.commit()
        response["status"] = "OK"
        settings = SystemSetting.get_settings()
        response["system_settings"] = schema.dump(settings).data
        return response, 200

