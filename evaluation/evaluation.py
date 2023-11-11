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

def recall_at_k(results: list, k: int) -> float:
    return len([
        result for result in results[:k] if result == 1
    ]) / len(results)

def precision_values(results: list) -> float:
    return [
        precision_at_k(results, k) for k in range(1, len(results) + 1)
    ]

def recall_values(results: list) -> float:
    return [
        recall_at_k(results, k) for k in range(1, len(results) + 1)
    ]

# MAP - Mean Average Precision
def mean_average_precision(stats) -> float:
    values = []
    for stat in stats:
        values.append(stat['AvP'])
    return sum(values) / len(stats)

# P@K - Precision At K
def precision_at_k(results: list, k: int = PRECISION_AT) -> float:
    return len([
        result for result in results[:k] if result == 1
    ]) / k

# AvP - Average Precision
def average_precision(results: list) -> float:
    precisions = precision_values(results)
    return round(sum(precisions) / len(results), 2)

# Recall
def recall(results: list) -> float:
    return round(sum(recall_values(results)), 2)

# Precision-Recall Curves
def precision_recall(results: list, mode: str, query: int) -> None:

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

    disp = PrecisionRecallDisplay([
        precision_recall_match.get(r) for r in recall_results
    ], recall_results)

    disp.plot()
    plt.savefig(f'./q{query}/p-r-curve-{mode}.png')
    plt.close()

def print_stats(stats: dict) -> None:
    for key, value in stats.items():
        print(f"{key}: {value}")

def evaluate(query: int, mode: str) -> None:

    results = getResults(query, mode)
    stats = {
        'query': f'q{query}',
        'mode': mode,
        'P@20': precision_at_k(results),
        'AvP': average_precision(results),
    }

    precision_recall(results, mode, query)
    print_stats(stats)

    return stats

if __name__ == "__main__":

    for mode in ['schemaless', 'boosted']:
        stats = []
        for query in range(1, 2): # ..5, only q1 for development/debug reasons
            stat = evaluate(query, mode)
            stats.append(stat)
        print(f'MAP: {mean_average_precision(stats)}\n')