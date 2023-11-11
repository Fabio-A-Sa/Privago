import json
import subprocess
import requests
import os 

CONTAINER_NAME = 'privago'
PARAMETERS = 'parameters.json'
REQUEST_BASE = 'http://localhost:8983/solr/hotels/select?'

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
    print(parameters)

    # Mock request
    return REQUEST_BASE + "defType=edismax&fl=*%2C%5Bchild%5D&indent=true&q.op=OR&q=*%3A*&rows=60&start=0&useParams="

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

    for mode in ['simple', 'boosted']:
        runContainer(mode)
        for index in range(1, 2): # ..5, only q1 for development/debug reasons
            query(index, mode)
        stopContainer()