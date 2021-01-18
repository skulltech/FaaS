from peewee import MySQLDatabase, Model, CharField
from config import Settings

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
    server = CharField(null=True)

    class Meta:
        database = db


db.create_tables([Function])
