from flask.cli import FlaskGroup

from app import create_app
from app.database import db

from app.api.user.models import User
from app.api.system.models import SystemSetting


app = create_app()
cli = FlaskGroup(create_app=create_app)
prompt = "> "


@cli.command('create_admin')
def create_admin_user():
    if not User.query.filter_by(is_admin=True).first():
        print("Username: ")
        username = input(prompt)
        print("Email: ")
        email = input(prompt)
        print("Password: ")
        pw1 = input(prompt)
        print("Password repeat: ")
        pw2 = input(prompt)

        if pw1 == pw2:
            user = User(username, pw1, email)
            user.is_admin = True
            user.save()
            print("Admin user created")
        else:
            print("Admin user already exists")

@cli.command('create_settings')
def create_sys_settings():
    if not SystemSetting.query.get(1):
        print("Kaffee Preis")
        kaffee_preis = input(prompt)

        systemSettings = SystemSetting(
            kaffee_preis=kaffee_preis
        )
        systemSettings.save()
    else:
        print("System Settings already exists")

if __name__ == '__main__':
    cli()
