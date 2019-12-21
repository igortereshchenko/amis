from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

class performer(Base):
    __tablename__='performer'
    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    album = relationship("album", back_populates="performer")

class album(Base):
    __tablename__='album'
    id = Column(Integer, primary_key=True)
    title = Column(String(15))
    performer_id = Column(Integer, ForeignKey('performer.id'))
    performer = relationship("performer", back_populates="album")
    melody = relationship("melody", back_populates="album")

class student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    faculty = Column(String(15))
    group = Column(String(8))
    surname = Column(String(15))
    name = Column(String(15))
    username = Column(String(36))
    wish = relationship("wish", back_populates="student")

class genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    psychotype = Column(String(15))
    melody = relationship("melody", back_populates="genre")

class melody(Base):
    __tablename__ = 'melody'
    id = Column(Integer, primary_key=True)
    title = Column(String(15))
    singer = Column(String(15))
    release_date = Column(Date)
    melody_genre = Column(Integer, ForeignKey('genre.id'))
    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship("album", back_populates="melody")
    wish = relationship("wish", back_populates="melody")
    genre = relationship("genre", back_populates="melody")

class wish(Base):
    __tablename__ = 'wish'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    wish_date = Column(Date)
    wish_performer = Column(String(15))
    wish_melody = Column(Integer, ForeignKey('melody.id'))
    wish_genre = Column(Integer)
    melody = relationship("melody", back_populates="wish")
    student = relationship("student", back_populates="wish")

# class ormGanre(Base):
#     __tablename__ = 'orm_ganre'
#     id=Column(Integer, primary_key=True)
#     name = Column(String(15))
#     popularity = Column(Integer)
#     count_of_subscribers = Column(Integer)
#     year = Column(Integer)
#     melody = relationship("ormMelody", back_populates="orm_ganre")
#
# class ormMelody(Base):
#     __tablename__ = 'orm_melody'
#     id=Column(Integer, primary_key=True)
#     genre_id=Column(Integer, ForeignKey('orm_ganre.id'))
#     melody_title = Column(String(15))
#     melody_singer = Column(String(15))
#     melody_genre = Column(String(15))
#     orm_ganre = relationship("ormGanre", back_populates="melody")

