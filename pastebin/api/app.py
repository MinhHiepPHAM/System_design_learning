import os, math
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import datetime
from base62 import encode, decode
from helper import display_relative_time, datetime_to_string, get_file_size
from elastic import set_index, create_index, search
from elasticsearch import Elasticsearch

load_dotenv()

app = Flask(__name__)
CORS(app)
es = Elasticsearch('http://localhost:9200', request_timeout=30)

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

    # get recent links
    cur.execute(
        'SELECT shortlink, created_at, pastepath FROM pastes ORDER BY id DESC LIMIT 20;'
    )


    recent_links = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            'shortlink': shortlink,
            'created_at': display_relative_time(created_at, datetime.datetime.now(datetime.timezone.utc)),
            'size': get_file_size(pastepath)
        }
        for shortlink, created_at, pastepath in recent_links   
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
    
    # use Elasticsearch to index the paste context to quickly find the path in
    # search engine
    index_name = f'index_{id_base62}'
    if not es.indices.exists(index=index_name):
        create_index(es, index_name)
    set_index(es, index_name, pastepath, paste_text)

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(shortlink=shortlink, status=200)

@app.route('/detail/<shortlink>')
def shortlink(shortlink):
    conn = get_db_connection()
    cur = conn.cursor()
    id = decode(shortlink)
    cur.execute(
        'SELECT created_at, pastepath, expiration FROM pastes WHERE id=%s;',(id, )
    )

    created_at, pastepath, expiration = cur.fetchall()[0]
    conn.close()
    cur.close()

    expired_at = datetime_to_string(datetime.timedelta(minutes=expiration) + created_at)

    with open(pastepath,'r') as f:
        context = f.read()
    
    return jsonify(
        expiration = expired_at,
        context = context, 
        size = get_file_size(pastepath)
    )

@app.route('/all')
def all_links():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM pastes;')
    total = cur.fetchone()[0]
    
    page_num = int(request.args.get('page',1))
    page_size = 20
    offset = (page_num-1) * page_size
    
    cur.execute(
        'SELECT shortlink, created_at, pastepath FROM pastes ORDER BY id DESC '
        'OFFSET %s LIMIT %s;', (offset,page_size)
    )

    link_infos = [{
        'shortlink': shortlink,
        'created_at': display_relative_time(created_at, datetime.datetime.now(datetime.timezone.utc)),
        'size': get_file_size(pastepath)
    }
    for shortlink, created_at, pastepath in cur.fetchall()   
    ]


    cur.close()
    conn.close()

    return jsonify(link_infos=link_infos, num_page=math.ceil(total/page_size), status=201)

@app.route('/search/<query>')
def search_result(query):
    conn = get_db_connection()
    cur = conn.cursor()

    # Better to use pagination to return the search result to limit the number
    # of pastes. This code is only for testing the elastic searach, so I get
    # all pastes in only one page
    response = []
    for filename in search(es, '*', query):
        base62_str = filename.split('/')[-2]
        id = decode(base62_str)
        cur.execute(
            'SELECT shortlink, created_at FROM pastes WHERE id=%s;', (id, )
        )

        shortlink, created_at = cur.fetchall()[0]
        filename = os.path.join('pastepath', base62_str, 'path.txt')
        with open(filename, 'r') as f:
            paste_context = f.read()
        response.append(
            {
                "shortlink": shortlink,
                "created_at": display_relative_time(created_at, datetime.datetime.now(datetime.timezone.utc)),
                'context': paste_context
            }
        )

    return jsonify(results=response, status=201)







