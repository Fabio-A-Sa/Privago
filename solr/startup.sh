#!/bin/bash

# Runing Solr container
# Creating a project "privago"
# Creating a virtual folder "data"
docker run -p 8983:8983 --name privago -v .:/data -d solr:9.3

# Creating a schema based on "schema.json" file into "privago" project
curl -X POST -H 'Content-type:application/json' --data-binary "@./schema.json" http://localhost:8983/solr/privago/schema

# Copy pipeline output to virtual "data" folder
cp ../data/processed/hotels_complete.json .

# Create "hotels" core inside "privago" project"
# Populate collection using mapped folder "data" and pipeline output
docker exec -it privago bin/post -c hotels /data/hotels_complete.json

# Removing always pipeline output for github/commits reasons
rm hotels_complete.json