from peewee import (
    MySQLDatabase,
    Model,
    CharField,
    ForeignKeyField,
    DateTimeField,
    BooleanField,
)
from config import Settings
import datetime

settings = Settings()

db = MySQLDatabase(
    settings.mysql_database,
    user=settings.mysql_user,
    password=settings.mysql_password,
    host=settings.mysql_server,
    port=3306,
)


class Function(Model):
    id = CharField(primary_key=True)
    handler = CharField()
    payload = CharField()

    class Meta:
        database = db


class Container(Model):
    id = CharField(primary_key=True)
    function = ForeignKeyField(Function, backref="containers")
    created_at = DateTimeField(default=datetime.datetime.now)
    stopped_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)

    class Meta:
        database = db


db.create_tables([Function, Container])
