import os
import psycopg2
from flask import Flask, request, Response
from flask_cors import CORS
from dotenv import load_dotenv
import datetime
from base62 import encode, decode


load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host = os.environ['HOST'],
        database = os.environ['DATABASE_NAME'],
        user = os.environ['USER_NAME'],
        password = os.environ['PASSWORD']
    )

    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    # get 10 recent links
    cur.execute(
        'SELECT shortlink, created_at FROM pastes ORDER BY created_at ASC LIMIT 10;'
    )

    recent_links = cur.fetchall()
    return [
        {'shortlink': shortlink, 'created_at': created_at}
        for shortlink, created_at in recent_links   
    ]

@app.route('/create/', methods=('POST',))
def create():
    data = request.get_json()
    paste_text = data.get('paste')
    created_at = datetime.datetime.now()
    expiration = data.get('expiration')

    conn = get_db_connection()
    cur = conn.cursor()
    created_at = datetime.datetime.now()

    cur.execute(
        'INSERT INTO pastes (id, expiration, created_at, shortlink, pastepath) '
        'VALUES (default, %s, %s, %s, %s) RETURNING id;',
        (expiration, created_at, '-', '-') 
    )


    new_id = cur.fetchone()[0]
    id_base62 = encode(new_id)
    if len(id_base62) < 8: id_base62 = 'a'*(8-len(id_base62)) + id_base62
    shortlink = 'http://localhost:5000/' + id_base62
    
    # Use txt file to store the paste context.
    # TODO: Store the file in AWS S3
    pastepath = os.path.join('pastepath', id_base62, 'path.txt') 
    
    cur.execute(
        'UPDATE pastes SET (shortlink, pastepath) = (%s, %s) WHERE id = %s',
        (id_base62, pastepath, new_id)
    )

    os.makedirs(os.path.join('pastepath', id_base62), exist_ok=True)


    with open(pastepath, 'w') as filename:
        filename.write(paste_text)

    conn.commit()
    cur.close()
    conn.close()

    return Response(status=200)



    


    




