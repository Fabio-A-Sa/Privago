import json

LIMIT = 60
PRECISION_AT = 20

def getResults(query: int, mode: str) -> list:
    path = f"./q{query}/evaluation-{mode}.json"
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
    
    results = data.values()
    assert len(results) == LIMIT
    return list(results)

# P@K
def precision_at_k(results: list, k: int = PRECISION_AT) -> float:
    return len([
        result for result in results[:k] if result == 1
    ]) / k

def recall_at_k(results: list, k: int) -> float:
    return len([
        result for result in results[:k] if result == 1
    ]) / len(results)

def precision_values(results: list) -> float:
    return [
        precision_at_k(results, k) for k in range(1, len(results)+ 1)
    ]

def recall_values(results: list) -> float:
    return [
        recall_at_k(results, k) for k in range(1, len(results)+ 1)
    ]

# MAP
def mean_average_precision() -> float:
    # interpretar a necessidade desta métrica no contexto global
    pass

# AvP
def average_precision(results: list) -> float:
    precisions = precision_values(results)
    return round(sum(precisions) / len(results), 2)

# Recall
def recall(results: list) -> float:
    return round(sum(recall_values(results)), 2)



def evaluate(query: int, mode: str) -> None:
    results = getResults(query, mode)
    print(f"Mode: {mode}")
    print(f"P@20: {precision_at_k(results)}")
    print(f"AvP: {average_precision(results)}")
    print(f"Recall: {recall(results)}")

if __name__ == "__main__":

    for mode in ['schemaless', 'boosted']:
        for query in range(1, 2): # ..5, only q1 for development/debug reasons
            evaluate(query, mode)