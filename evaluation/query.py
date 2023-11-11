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

def query(query: int, mode: str) -> None:
    path = f"./q{query}"
    print(getParameters(query))

if __name__ == '__main__':

    for mode in ['schemaless', 'boosted']:
        runContainer(mode)
        for index in range(1, 5):
            query(index, mode)
        stopContainer()