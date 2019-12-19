from dao.orm.model import *
from dao.db import PostgresDb

db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

session.query(student).delete()
session.query(genre).delete()
session.query(performer).delete()
session.query(album).delete()
session.query(melody).delete()
session.query(wish).delete()


session.commit()
# #clear all tables in right order
# session.query(ormMelody).delete()
# session.query(ormGanre).delete()
#
#
# pop = ormGanre(id=1,name = 'pop', popularity = 10000, count_of_subscribers = 10000, year = 2004)
# indie = ormGanre(id=2,name = 'indie', popularity = 10, count_of_subscribers = 10, year = 2007)
# rock = ormGanre(id=3,name = 'rock', popularity = 100, count_of_subscribers = 100, year = 2018)
#
# aaa = ormMelody(id=1,genre_id=2,melody_title = 'AAA', melody_singer = 'Mur', melody_genre = 'indie')
# haisfisch = ormMelody(id=2,genre_id=3,melody_title = 'Haisfisch', melody_singer = 'Ramst', melody_genre = 'rock')
# ccc = ormMelody(id=3,genre_id=2,melody_title = 'CCC', melody_singer = 'Mur', melody_genre = 'indie')
#
# session.add_all([pop, indie, rock, aaa, haisfisch, ccc])
# session.commit()
# session.query(association_table).delete()
#
# ukr_asoc = association_table(ormperformer_id='Ukraine', ormcountry_id='Ukraine')
# england_asoc = association_table(ormperformer_id='England', ormcountry_id='England')
# poland_asoc = association_table(ormperformer_id='Poland', ormcountry_id='Poland')
#
# Ukraine = ormCountry(name='Ukraine', population=602, goverment='демократичне', location='50 30')
# England = ormCountry(name='England', population=702, goverment='демократичне', location='0 20')
# Poland = ormCountry(name='Poland', population=402, goverment='унітарне', location='30 30')
#
# a = ormPerformer(name='Lambert', country='Ukraine')
# b = ormPerformer(name='Boba', country='Poland')
# c = ormPerformer(name='ccc', country='Ukraine')
#
# session.add_all([a, b, c, Ukraine, England, Poland])
# session.commit()