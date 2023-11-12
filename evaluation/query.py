import json
import subprocess
import requests
import os 
import sys
import urllib.parse

CONTAINER_NAME = 'privago'
PARAMETERS = 'parameters.json'
REQUEST_BASE = 'http://localhost:8983/solr/hotels/select?'
QUERIES = 4
MODES = ['simple', 'boosted']

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

    if len(sys.argv) == 1:

        for mode in MODES:
            runContainer(mode)
            for index in range(1, QUERIES + 1):
                query(index, mode)
            stopContainer()

    elif len(sys.argv) == 2 and 1 <= int(sys.argv[1]) <= QUERIES:
        
        for mode in MODES:
            runContainer(mode)
            query(int(sys.argv[1]), mode)
            stopContainer()

    else:
        print("Bad arguments. Usage: python3 query.py [N]")