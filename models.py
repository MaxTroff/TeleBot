from peewee import (
    AutoField,
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    DateTimeField
)

from config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    """
    Дочерний класс-модель с данными пользователя;
    Родитель: Model
    """
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)

class Command(BaseModel):
    user = ForeignKeyField(User, backref='history')
    request_id = AutoField()
    command = CharField()

    def __str__(self):
        "{}".format(str(self.command))

class CommandParameters(BaseModel):
    command = ForeignKeyField(Command)
    name = CharField()
    value = CharField()

def create_models() -> None:
    """
    Функция создания таблицы базы данных
    :return: None
    """
    db.create_tables(BaseModel.__subclasses__())