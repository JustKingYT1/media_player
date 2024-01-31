import peewee

import sys

sys.path.append('../media_player')

from src.settings import DB_PATH, DB_NAME, DEBUG


db = peewee.SqliteDatabase(database=f'{DB_PATH}/{DB_NAME}')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Musics(BaseModel):
    author = peewee.CharField()
    name = peewee.CharField()
    time = peewee.CharField()

if DEBUG:
    db.create_tables([Musics,])

    Musics.create(author='Avtor_1', name='music_2', time='2:29')
    Musics.create(author='Avtor_2', name='music_1', time='2:01')
    Musics.create(author='Avtor_1', name='music_3', time='3:01')
        