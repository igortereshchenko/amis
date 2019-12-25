from dal.credentials import BASE, USERNAME, PASSWORD, HOST, PORT, DATABASE

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#db_string = 'postgres://ugunknjzriwlkd:93b58b7377690b9b3f72fc04d7f7670c33404aec85512517c9f9547f62237ff3@ec2-54-247-70-127.eu-west-1.compute.amazonaws.com:5432/d2a4qrjvkbkkkk'
db_string = '{base}://{user}:{pw}@{host}:{port}/{db}'.format(base=BASE,user=USERNAME,pw=PASSWORD,host=HOST,port=PORT,db=DATABASE)

engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()

metadata = Base.metadata
