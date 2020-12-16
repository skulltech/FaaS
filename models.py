from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase("FaaS.db")


class Function(Model):
    id = CharField(primary_key=True)
    handler = CharField()
    server = CharField(null=True)
    image = CharField(null=True)
    container = CharField(null=True)

    class Meta:
        database = db


db.create_tables([Function])
