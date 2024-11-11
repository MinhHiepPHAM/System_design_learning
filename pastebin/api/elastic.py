import os


def set_index(es, index_name, filename, context):
    document = {
        "filename": filename,
        "content": context
    }

    es.index(index=index_name, body=document)

def create_index(es, index_name):
    es.indices.create(index=index_name, body={
        "settings": {
        "number_of_shards": 1,  # Reduce shard count as needed
        "number_of_replicas": 1
        }
    })


def search(es, index_name, text):
    search_query = {
        "query": {
            "match": {
                "content": f"{text}"
            }
        }
    }
    for hit in es.search(index=index_name, body=search_query)["hits"]["hits"]:
        yield hit["_source"]["filename"]

    

    

