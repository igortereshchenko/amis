from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from LecturebotDAL import dbconnection


connection_string = '{base}://{user}:{pw}@{host}:{port}/{db}'.format(
    base=dbconnection.BASE,
    user=dbconnection.USERNAME,
    pw=dbconnection.PASSWORD,
    host=dbconnection.HOST,
    port=dbconnection.PORT,
    db=dbconnection.DATABASE
)

DBEngine = create_engine(connection_string)
Session = sessionmaker(bind=DBEngine)

ModelBase = declarative_base()
session = Session()

class PostgresDb(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                connection = psycopg2.connect(host='ec2-107-21-255-181.compute-1.amazonaws.com',
                                              database='d1joakede3ro0p', user='aeeneklhkrnneh', password='178049f753ac3154137f98c8d0bd4045ab19819cf294d73ce59e9b510c9e248f')
                cursor = connection.cursor()

                # execute a statement
                print('PostgreSQL database version:')
                cursor.execute('SELECT version()')

                # display the PostgreSQL database server version
                db_version = cursor.fetchone()
                print(db_version)

                engine = create_engine(connection_string)

                Session = sessionmaker(bind=engine)
                session = Session()

                PostgresDb._instance.sqlalchemy_session = session
                PostgresDb._instance.sqlalchemy_engine = engine

            except Exception as error:
                print('Error: connection not established {}'.format(error))

        return cls._instance

    def __init__(self):
        engine = create_engine(connection_string)

        Session = sessionmaker(bind=engine)
        session = Session()

        self.sqlalchemy_session = session
        self.sqlalchemy_engine = engine

    def __del__(self):
        self.sqlalchemy_session.close()


if __name__ == "__main__":
    db = PostgresDb()