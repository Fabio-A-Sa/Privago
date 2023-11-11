import json
import requests

PARAMETERS = 'parameters.json'
DOCUMENTS_LIMIT = 60

def getParameters(query: int) -> json:
    with open(PARAMETERS, 'r') as file:
        data = json.load(file)
        file.close()

    return data.get(f'q{query}', {})

def query(query: int, type: str) -> None:
    path = f"./q{query}"
    print(getParameters(query))

if __name__ == '__main__':

    # Run Solr - Schemaless mode    


    for index in range(1, 5):
        query(index, 'schemaless')

    # Stop Solr

    # Run Solr - Boosted mode


    for index in range(1, 5):
        query(index, 'boosted')
    
    # Stop Solr