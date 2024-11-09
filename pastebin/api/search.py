import os
from elasticsearch import Elasticsearch, helpers
from base62 import decode

es = Elasticsearch('http://localhost:9200', timeout=30)
PASE_REPO = 'pastepath'

def find_pastepath():
    for root, dirs, files in os.walk(PASE_REPO):
        for file in files:
            yield os.path.join(root, file)

def create_index(index_name):
    es.indices.create(index=index_name, body={
        "settings": {
        "number_of_shards": 1,  # Reduce shard count as needed
        "number_of_replicas": 1
        }
    })

def set_index_older_created_file():
    for filename in find_pastepath():
        with open(filename, 'r',encoding='utf-8') as file:
            for line_number, line_content in enumerate(file, start=1):
                document = {
                    "filename": filename,
                    "line_number": line_number,
                    "content": line_content.strip()
                }
                link = filename.split('/')[1]
                index_name = f'index_{decode(link)}'
                # Index the document
                if not es.indices.exists(index=index_name):
                    create_index(index_name)
                es.index(index=index_name, body=document)
            

if __name__ == '__main__':
    if not es.ping():
        raise ValueError("Connection to Elasticsearch failed")
    es.indices.delete(index='*') 
    et_index_older_created_file()
    
    search_query = {
        "query": {
            "match": {
                "content": "pdf"
            }
        }
    }


    response = es.search(index='*', body=search_query)
    for hit in response["hits"]["hits"]:
        print(f'{hit["_source"]["filename"]}')



