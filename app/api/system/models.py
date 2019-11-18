from app.database import db, BaseMixin
from app.serializer import ma


class SystemSetting(db.Model, BaseMixin):
    __tablename__ = "systemSettings"
    sys_email = db.Column(db.String(60))
    sys_email_pw = db.Column(db.String(60))
    sys_email_host = db.Column(db.String(60))
    sys_email_port = db.Column(db.Integer)
    sys_email_tls = db.Column(db.Boolean)
    kaffee_preis = db.Column(db.Float)

    def __init__(self, kaffee_preis):
        self.kaffee_preis = kaffee_preis

    @classmethod
    def get_settings(cls):
        return cls.query.get(1)


class SystemSettingSchema(ma.ModelSchema):
    class Meta:
        model = SystemSetting
        fields = (
            "id",
            "sys_email",
            "sys_email_pw",
            "sys_email_host",
            "sys_email_port",
            "sys_email_tls",
            "kaffee_preis"
        )
    