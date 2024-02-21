import peewee

import sys

sys.path.append('../media_player')

from settings import DB_PATH, DB_NAME, DEBUG


db = peewee.SqliteDatabase(database=f'{DB_PATH}/{DB_NAME}')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Musics(BaseModel):
    author = peewee.CharField()
    name = peewee.CharField()
    path = peewee.CharField(unique=True)
    class Meta:
        database = db
        indexes = (
            (('author', 'name'), True),
        )


class Users(BaseModel):
    password = peewee.CharField()
    username = peewee.CharField(unique=True)


class UserPlaylists(BaseModel):
    user_id = peewee.ForeignKeyField(Users, backref='playlists')
    music_id = peewee.ForeignKeyField(Musics, backref='playlists')
    class Meta:
        database = db
        indexes = (
            (('user_id', 'music_id'), True),
        )


if DEBUG:
    db.create_tables([Musics, Users, UserPlaylists])
        