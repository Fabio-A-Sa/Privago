import json
import subprocess
import requests

CONTAINER_NAME = 'privago'
PARAMETERS = 'parameters.json'

def getParameters(query: int) -> json:
    with open(PARAMETERS, 'r') as file:
        data = json.load(file)
        file.close()

    return data.get(f'q{query}', {})

def runContainer(mode: str) -> None:
    script = f"../solr/startup_{mode}.sh"
    subprocess.run(["bash", script])

def stopContainer() -> None:
    subprocess.run(["docker", "stop", "privago"])
    subprocess.run(["docker", "rm", "privago"])

def getRequest(parameters: json):
    return "localhost:5000/solr/hotels/?q=something" # TODO

def query(query: int, mode: str) -> None:
    path = f"./q{query}/result-{mode}.json"
    parameters = getParameters(query)
    request = getRequest(parameters)
    result = requests.get(request)

    with open(path, 'w') as file:
        file.write(result)
        file.close()

if __name__ == '__main__':

    for mode in ['schemaless', 'boosted']:
        runContainer(mode)
        for index in range(1, 5):
            query(index, mode)
        stopContainer()