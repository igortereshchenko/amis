import datetime

from dao.orm.model import *
from dao.db import PostgresDb

db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

session.query(wish).delete()
session.query(melody).delete()
session.query(album).delete()
session.query(student).delete()
session.query(genre).delete()
session.query(performer).delete()

Atamanchuk = student(id=1, faculty='FICT', group='IT-61', surname='Atamanchuk', name='Lena', username='@nechla')
Yaremchuk = student(id=2, faculty='IASA', group='KA-65', surname='Yaremchuk', name='Daniel', username='@reya')
Varzhansky = student(id=3, faculty='FMM', group='FF-91mn', surname='Varzhansky', name='Illya', username='@ilyavl')
Kovtonyuk = student(id=4, faculty='FICT', group='IO-63', surname='Kovtonyuk', name='Vova', username='@kovla')
Palyokha = student(id=5, faculty='FICT', group='IT-61', surname='Palyokha', name='Sasha', username='@pasha')
Lutska = student(id=6, faculty='FICT', group='II-62', surname='Lutska', name='Liza', username='@lutskayaliz')
Kubenko = student(id=7, faculty='FMM', group='FF-82', surname='Kubenko', name='Masha', username='@kubomash')
Samsoniuk = student(id=8, faculty='IASA', group='KA-61', surname='Samsoniuk', name='Petya', username='@samsopet')
Popova = student(id=9, faculty='IASA', group='KA-64', surname='Popova', name='Rita', username='@ri_ta_po')

pop = genre(id=1, name='pop', psychotype='gipertim')
indie = genre(id=2, name='indie', psychotype='emotive')
rock = genre(id=3, name='rock', psychotype='isteroid')
romans = genre(id=4, name='romans', psychotype='disturbing')
classic = genre(id=5, name='classic', psychotype='PSYCHASTENOID')
blues = genre(id=6, name='blues', psychotype='emotive')
jazz = genre(id=7, name='jazz', psychotype='gipertim')

Elzy = performer(id=1, name='Okean Elzy')
Hardkiss = performer(id=2, name='The Hardkiss')
Babkin = performer(id=3, name='Serhii Babkin')
Zemfira = performer(id=4, name='Zemfira')
Jackson = performer(id=5, name='Michael Jackson')

no_album1 = album(id=0, title='Blues', performer_id=4)
Zemlya = album(id=1, title='Zemlya', performer_id=1)
Closer = album(id=2, title='Closer', performer_id=2)
Muzasfera = album(id=3, title='Muzasfera', performer_id=3)
no_album2 = album(id=4, title='Smooth Criminal', performer_id=5)

Prirva = melody(id=1, title='Prirva', singer='The Hardkiss', release_date=datetime.date(2016, 4, 19), melody_genre=4,album_id=2)
Blues = melody(id=2, title='Blues', singer='Zemfira', release_date=datetime.date(2009, 12, 30), melody_genre=6,album_id=0)
Criminal = melody(id=3, title='Smooth Criminal', singer='Michael Jackson', release_date=datetime.date(1997, 11, 5), melody_genre=1,album_id=4)

atam1912 = wish(id=1, student_id=1, wish_date=datetime.date(2019, 12, 19), wish_performer='Zemfira', wish_melody=2,wish_genre=6)
kovt1912 = wish(id=2, student_id=4, wish_date=datetime.date(2019, 12, 19), wish_performer='', wish_melody=3,wish_genre=1)
paly1812 = wish(id=3, student_id=5, wish_date=datetime.date(2019, 12, 18), wish_performer='', wish_melody=2,wish_genre=6)
kube1612 = wish(id=4, student_id=7, wish_date=datetime.date(2019, 12, 16), wish_performer='', wish_melody=2,wish_genre=6)
session.add_all([Atamanchuk,Yaremchuk,Varzhansky,Kovtonyuk,Palyokha,Lutska,Kubenko,Samsoniuk,Popova,pop,indie,rock,romans,classic,blues,jazz,
                 Elzy,Hardkiss,Babkin,Zemfira,Jackson,no_album1,Zemlya,Closer,Muzasfera,no_album2,Prirva,Blues,Criminal,atam1912,kovt1912,
                 paly1812, kube1612])

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