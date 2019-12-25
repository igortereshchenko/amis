import os

username = 'postgres'
password = 'Vladik99'
hostname = '127.0.0.1'
port = 5432
database_name = 'Testing'
DATABASE_URI = os.getenv("DATABASE_URL", f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}")