import json

PRECISION_AT = 20

def getResults(query: int, mode: str) -> list:
    path = f"./q{query}/evaluation-{mode}.json"
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
    
    results = data.values()
    assert len(results) == 60
    return list(results)

def precision_at_k(results: list) -> float:
    return len([
        result for result in results[:PRECISION_AT] if result == 1
    ]) / PRECISION_AT

def average_precision(results: list) -> float:
    return 10

def evaluate(query: int, mode: str) -> None:
    results = getResults(query, mode)
    print(precision_at_k(results))

if __name__ == "__main__":

    for mode in ['schemaless', 'boosted']:
        for query in range(1, 2): # ..5, only q1 for development/debug reasons
            evaluate(query, mode)