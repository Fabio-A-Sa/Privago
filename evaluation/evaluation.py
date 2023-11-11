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

# P@K
def precision_at_k(results: list, k: int = PRECISION_AT) -> float:
    return len([
        result for result in results[:k] if result == 1
    ]) / k

# AvP
def average_precision(results: list) -> float:
    precisions = 0
    for index in range(0, len(results)):
        precisions += precision_at_k(results, index + 1)

    return round(precisions / len(results), 2)

def evaluate(query: int, mode: str) -> None:
    results = getResults(query, mode)
    print(f"Mode: {mode}")
    print(f"P@20: {precision_at_k(results)}")
    print(f"AvP: {average_precision(results)}")

if __name__ == "__main__":

    for mode in ['schemaless', 'boosted']:
        for query in range(1, 2): # ..5, only q1 for development/debug reasons
            evaluate(query, mode)