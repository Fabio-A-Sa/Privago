import json
import subprocess
import requests
import os 

CONTAINER_NAME = 'privago'
PARAMETERS = 'parameters.json'
REQUEST_BASE = 'http://localhost:8983/solr/hotels/select?'

def getParameters(query: int) -> json:
    with open(PARAMETERS, 'r') as file:
        data = json.load(file)
        file.close()

    return data.get(f'q{query}', {})

def runContainer(mode: str) -> None:

    current_dir = os.getcwd()
    try:
        os.chdir("../solr")
        subprocess.run(["bash", f"startup_{mode}.sh"])
    finally:
        os.chdir(current_dir)

    os.chdir("../evaluation")

def stopContainer() -> None:
    subprocess.run(["docker", "stop", CONTAINER_NAME])
    subprocess.run(["docker", "rm", CONTAINER_NAME])

def getRequest(parameters: json):
    # Mock request
    return REQUEST_BASE + "defType=edismax&fl=*%2C%5Bchild%5D&indent=true&q.op=OR&q=*%3A*&rows=60&start=0&useParams="

def query(query: int, mode: str) -> None:
    path = f"./q{query}/result-{mode}.json"
    parameters = getParameters(query)
    request = getRequest(parameters)
    result = json.dumps(requests.get(request).json())

    with open(path, 'w') as file:
        file.write(result)
        file.close()

if __name__ == '__main__':

    for mode in ['schemaless', 'boosted']:
        runContainer(mode)
        for index in range(1, 2): # ..4, only q1 for development/debug reasons
            query(index, mode)
        stopContainer()