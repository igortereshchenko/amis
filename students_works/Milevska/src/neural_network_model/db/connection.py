import psycopg2
from dao.credentials import *

conn = psycopg2.connect(
    host=host,
    port=port,
    database=database_name,
    user=username,
    password=password
)

# cursor = conn.cursor()
