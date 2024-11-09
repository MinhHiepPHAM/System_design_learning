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


