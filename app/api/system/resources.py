import json
import pika
import logging
from flask import request
from flask_restful import Resource

from app.security import admin_required
from app.database import db
from app.api.system.models import SystemSetting, SystemSettingSchema
from app.api.user.models import User

logging.basicConfig(level=logging.WARNING)
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


class RechnungsApi(Resource):

    @admin_required
    def put(self):
        # /admin/rechnungslauf
        data = request.get_json()
        settings = SystemSetting.get_settings()

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()
        channel.queue_declare(queue="email")
            
        for each in data:
            settings = SystemSetting.get_settings()
            logging.warning(f"Using: {each}")
            logging.warning(f"username: {each['username']}, coffee_count: {each['coffee_count']}")
            obj = {
                "username": "",
                "email": "",
                "coffee_count": "",
                "betrag": ""
            }
            logging.warning("Rechne new_coffee_count aus")
            new_coffee_count = RechnungsApi.count(each['coffee_count'])
            if new_coffee_count is None:
                new_coffee_count = int(0)
            logging.warning(f"New coffee count: {new_coffee_count}")
            logging.warning("Getting user")
            user = User.find_by_username(each['username'])
            logging.warning(f"Found user: {user.username}")
            logging.warning(f"User coffee count: {user.coffee_count}")
            temp_var = user.coffee_count - new_coffee_count
            logging.warning(f"Temporary coffee_count: {temp_var}")
            user.coffee_count = temp_var
            user.save()
            obj["username"] = user.username
            obj["email"] = user.email
            obj["coffee_count"] = new_coffee_count
            obj["betrag"] = new_coffee_count * settings.kaffee_preis
            logging.warning(f"obj: {obj}")
            user = User.find_by_username(each['username'])
            logging.warning(f"Neuer User coffee counter: {user.coffee_count}")
            channel.basic_publish(
                exchange="",
                routing_key="email",
                body=json.dumps(obj)
            )
        connection.close()
        return {
            "message": "Die Daten wurden gespeichert und Emails werden versendet."
        }, 201

            

        #for each in data
            #create new user_obj
            #schleife um coffee_count % 5 == 0 herauszufinden, wenn nicht dann coffee_count -= 1
            #get user > coffee_count - coffees > speichern den neuen Wert
            #multiply coffee_count * coffee_price > save to user_obj
            #save user_email, username to user_obj
            #create object in queue for email

    @staticmethod
    def count(nummer):
        rest = int(nummer) % 5
        if rest == 0:
            return nummer
        else:
            nummer = int(nummer) - 1
            RechnungsApi.count(nummer)