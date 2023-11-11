import json

def getResults(query: int, mode: str) -> list:
    path = f"./q{query}/evaluation-{mode}.json"
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
    
    return list(data.values())

def evaluate(query: int, mode: str) -> None:
    results = getResults(query, mode)
    assert len(results) == 60
    print(results)

if __name__ == "__main__":

    for mode in ['schemaless', 'boosted']:
        for index in range(1, 2): # ..5, only q1 for development/debug reasons
            evaluate(index, mode)