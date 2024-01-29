import peewee

import sys

sys.path.append('../music_player_app')

from src.settings import DB_PATH, DB_NAME


db = peewee.SqliteDatabase(database=f'{DB_PATH}/{DB_NAME}')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Musics(BaseModel):
    author = peewee.CharField()
    name = peewee.CharField()
    time = peewee.CharField()


db.create_tables([Musics,])

Musics.create(author='Avtor_1', name='Music_2', time='2:29')
Musics.create(author='Avtor_2', name='Music_1', time='2:01')
Musics.create(author='Avtor_1', name='Music_3', time='3:01')
    
# models_list = []

# for model in Musics.select():
#     new_model = {}
#     for attr in ['author', 'name', 'time']:
#         get_attr = getattr(model, attr)
#         new_model[attr] = get_attr
#     models_list.append(new_model)

# print(len(Musics.select()))