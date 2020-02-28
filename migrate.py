from pyArango.connection import Connection
from elasticsearch import Elasticsearch
from settings import ES_HOST, ES_INDEX, ARANGO_ROOT_PASSWORD, ARANGO_USERNAME, ARANGO_COLLECTION


def main():
    assert ES_INDEX
    assert ES_HOST
    assert ARANGO_ROOT_PASSWORD
    assert ARANGO_COLLECTION
    assert ARANGO_USERNAME
    es = Elasticsearch([ES_HOST])
    conn = Connection(username=ARANGO_USERNAME, password=ARANGO_ROOT_PASSWORD)
    if ES_INDEX not in conn.databases:
        conn.createDatabase(name=ES_INDEX)
    db = conn[ES_INDEX]
    if not db.hasCollection(ARANGO_COLLECTION):
        db.createCollection(name=ARANGO_COLLECTION)

    # existed_patents_files = [
    # _file key for _file in db.AQLQuery(f"FOR doc IN {ARANGO_COLLECTION} RETURN doc", rawResults=True)
    # ]
    # import ipdb; ipdb.set_trace()

    res = es.search(index=ES_INDEX, body={"query": {"match_all": {}}})
    aql_query_insert = f"INSERT @doc INTO {ARANGO_COLLECTION} LET newDoc = NEW RETURN newDoc"
    for hit in res['hits']['hits']:
        hit['_file'] = hit['_id']
        db.AQLQuery(aql_query_insert, bindVars={'doc': hit})


if __name__ == '__main__':
    main()