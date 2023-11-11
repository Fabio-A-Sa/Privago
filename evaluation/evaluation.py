import json
import requests

PARAMETERS = 'parameters.json'

def getParameters(query: int) -> json:
    with open(PARAMETERS, 'r') as file:
        data = json.load(file)
        file.close()

    return data.get(f'q{query}', {})

def evaluation(query: int) -> None:
    path = f"./q{query}"
    print(getParameters(query))

if __name__ == '__main__':
    for query in range(1, 5):
        evaluation(query)