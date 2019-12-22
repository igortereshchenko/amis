import os

username = 'xujoczxbviwzjo'
password = '83a4ab01c63234f37abb82fabf8294c7f26494fdd92b567ead595ea821a3abba'
host = 'ec2-174-129-24-148.compute-1.amazonaws.com'
port = '5432'
database = 'dbriles54vm09o'
DATABASE_URI = os.getenv("DATABASE_URL",
                         'postgres://xujoczxbviwzjo:83a4ab01c63234f37abb82fabf8294c7f26494fdd92b567ead595ea821a3abba@ec2-174-129-24-148.compute-1.amazonaws.com:5432/dbriles54vm09o')