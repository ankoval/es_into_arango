#!/bin/sh
until $(curl --output /dev/null --silent --head --fail ${ATLAS_API_ELASTICSEARCH_DSL}); do
    printf '.'
    sleep 5
done

cd fixtures
curl -X PUT "${ATLAS_API_ELASTICSEARCH_DSL}/patents_test_index"
curl -s -H "Content-Type: application/json" -XPUT localhost:9200/patents_test_index/_mapping/_doc --data-binary "@mapping.json"
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary "@json_dump.json"
