import os

username = ''
password = ''
host = 'localhost'
port = '5432'
database = 'mydb'
DATABASE_URI = os.getenv("DATABASE_URL",
                         'postgres+psycopg2://postgres:{}@{}:{}/{}'.format(password, host, port, database))
