import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay

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

def precision_recall(results: list) -> None:

    precision_results = precision_values(results)
    recall_results = recall_values(results)
    precision_recall_match = {k: v for k,v in zip(recall_results, precision_results)}

    recall_results.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_results])
    recall_results = sorted(set(recall_results))

    for idx, step in enumerate(recall_results):
        if step not in precision_recall_match:
            if recall_results[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_results[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_results[idx+1]]

    disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_results], recall_results)
    disp.plot()
    plt.savefig('precision_recall.png')

def evaluate(query: int, mode: str) -> None:
    results = getResults(query, mode)
    print(f"Mode: {mode}")
    print(f"P@20: {precision_at_k(results)}")
    print(f"AvP: {average_precision(results)}")
    print(f"Recall: {recall(results)}")

    precision_recall(results)

if __name__ == "__main__":

    for mode in ['schemaless', 'boosted']:
        for query in range(1, 2): # ..5, only q1 for development/debug reasons
            evaluate(query, mode)