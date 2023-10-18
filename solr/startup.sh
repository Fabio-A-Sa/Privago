#!/bin/bash

# This script expects a container started with the following command.
docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9.3 solr-precreate courses

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./simple_schema.json" \
    http://localhost:8983/solr/courses/schema

# Populate collection using mapped path inside container.
docker exec -it meic_solr bin/post -c courses /data/meic_courses.json