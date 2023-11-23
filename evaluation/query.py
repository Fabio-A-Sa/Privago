import json
import subprocess
import requests
import os 
import sys
import urllib.parse

CONTAINER_NAME = 'privago'
PARAMETERS = 'parameters.json'
REQUEST_BASE = 'http://localhost:8983/solr/hotels/select?'
QUERIES = 8

MODES = {
    'm2': ['simple', 'boosted'],
    'm3': ['boosted', 'stopwords', 'semantic', 'final']
}

CONFIG = {
    'simple': [1, 4],
    'boosted': [1, 8],
    'stopwords': [5, 8],
    'semantic': [5, 8],
    'final': [5, 8]
}

def getParameters(query: int, mode: str) -> json:
    path = f"./q{query}/{PARAMETERS}"
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()

    return data.get(mode, {})

def runContainer(mode: str) -> None:
    current_dir = os.getcwd()
    try:
        os.chdir("../solr")
        subprocess.run(["bash", f"startup-{mode}.sh"])
    finally:
        os.chdir(current_dir)

    os.chdir("../evaluation")

def stopContainer() -> None:
    subprocess.run(["docker", "stop", CONTAINER_NAME])
    subprocess.run(["docker", "rm", CONTAINER_NAME])

def getRequest(parameters: json) -> str:
    query_string = urllib.parse.urlencode(parameters, quote_via=urllib.parse.quote)
    return REQUEST_BASE + query_string

def query(query: int, mode: str) -> None:
    path = f"./q{query}/result-{mode}.json"
    parameters = getParameters(query, mode)
    request = getRequest(parameters)
    result = requests.get(request).json()
    docs = result.get("response", {}).get("docs", [])

    with open(path, 'w') as file:
        file.write(json.dumps(docs, indent=2))
        file.close()

if __name__ == '__main__':

    # Run all queries (1, 2, 3, 4, 5, 6, 7, 8)
    if len(sys.argv) == 1:

        for mode in CONFIG:
            runContainer(mode)
            [min, max] = CONFIG[mode]
            for index in range(min, max + 1):
                query(index, mode)
            stopContainer()

    # Run all M2 or M3 queries (1, 2, 3, 4) or (5, 6, 7, 8)
    elif len(sys.argv) == 2 and sys.argv[1].lower() in ['m2', 'm3']:
        
        for mode in MODES[sys.argv[1].lower()]:
            runContainer(mode)
            [min, max] = CONFIG[mode]
            for index in range(min, max + 1):
                query(index, mode)
            stopContainer()

    # Run a single query
    elif len(sys.argv) == 2 and 1 <= int(sys.argv[1]) <= QUERIES:
        
        modes = MODES['m2'] if int(sys.argv[1]) < 5 else MODES['m3']
        for mode in modes:
            runContainer(mode)
            query(int(sys.argv[1]), mode)
            stopContainer()

    # Error
    else:
        print("Bad arguments. Usage:")
        print("    python3 query.py [N]      - to run a single query")
        print("    python3 query.py M<2,3>   - to run all milestone queries")
        print("    python3 query.py          - to run all queries (1, 2, 3, 4, 5, 6, 7, 8)")