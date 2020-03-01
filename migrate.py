import logging

from pyArango.connection import Connection
from elasticsearch import Elasticsearch
from settings import ES_HOST, ES_INDEX, ARANGO_ROOT_PASSWORD, ARANGO_USERNAME, ARANGO_COLLECTION, ARANGO_URL


def main():
    assert ES_INDEX
    assert ES_HOST
    assert ARANGO_URL
    assert ARANGO_ROOT_PASSWORD
    assert ARANGO_COLLECTION
    assert ARANGO_USERNAME

    es = Elasticsearch([ES_HOST])
    conn = Connection(arangoURL=ARANGO_URL, username=ARANGO_USERNAME, password=ARANGO_ROOT_PASSWORD)

    if ES_INDEX not in conn.databases:
        conn.createDatabase(name=ES_INDEX)
    db = conn[ES_INDEX]

    if not db.hasCollection(ARANGO_COLLECTION):
        db.createCollection(name=ARANGO_COLLECTION)

    existed_patents = db.AQLQuery(f"FOR doc IN {ARANGO_COLLECTION} RETURN doc._file").response['result']
    es_query_exclude_existed = {"query": {"bool": {"must_not": [{"ids": {"values": existed_patents}}]}}}
    res = es.search(index=ES_INDEX, body=es_query_exclude_existed)

    aql_query_insert = f"INSERT @doc INTO {ARANGO_COLLECTION} LET newDoc = NEW RETURN newDoc"
    for hit in res['hits']['hits']:
        hit['_file'] = hit['_id']
        db.AQLQuery(aql_query_insert, bindVars={'doc': hit})
        logging.info(f"Added: {hit['_file']}")


if __name__ == '__main__':
    main()
