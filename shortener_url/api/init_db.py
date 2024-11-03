import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

HOST = os.environ['HOST']
DATABASE = os.environ['DATABASE_NAME']
USERNAME = os.environ['USER_NAME']
PASSWORD = os.environ['PASSWORD']

conn = psycopg2.connect(
    host = HOST,
    database = DATABASE,
    user = USERNAME,
    password = PASSWORD

)

cur = conn.cursor()

cur.execute(
    'CREATE TABLE IF NOT EXISTS pastes ('
        'id SERIAL PRIMARY KEY,'
        'expiration integer NOT NULL,' # expiration in minuites
        'created_at TIMESTAMP WITH TIME ZONE NOT NULL,'
        'shortlink VARCHAR(10) UNIQUE NOT NULL,'
        'pastepath VARCHAR(255) NOT NULL);'
)

conn.commit()
cur.close()
conn.close()
