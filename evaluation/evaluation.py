import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import sys

LIMIT = 20
PRECISION_AT = 20
QUERIES = 4

MODES = {
    'm2': ['simple', 'boosted'],
    'm3': ['boosted', 'stopwords', 'semantic', 'final']
}

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
        len([
            doc for doc in results[:idx] if doc == 1
        ]) / idx 
        for idx, _ in enumerate(results, start=1)
    ]

def recall_values(results: list) -> float:
    return [
        len([
            doc for doc in results[:idx] if doc == 1
        ]) / sum(results)
        for idx, _ in enumerate(results, start=1)
    ]

# MAP
def mean_average_precision(stats):

    result = {"simple": 0, "boosted": 0}
    count_simple = 0
    count_boosted = 0
    
    for entry in stats:
        mode = entry["mode"]
        average_precision = entry["AvP"]
        
        if mode == "simple":
            result["simple"] += average_precision
            count_simple += 1
        elif mode == "boosted":
            result["boosted"] += average_precision
            count_boosted += 1

    result["simple"] /= count_simple if count_simple > 0 else 1
    result["boosted"] /= count_boosted if count_boosted > 0 else 1
    
    return result

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

    precision_results_k = [precision_recall_match.get(r) for r in recall_results]
    disp = PrecisionRecallDisplay(precision=precision_results_k, recall=recall_results)

    disp.plot()
    plt.xlim([0, 1.1])
    plt.ylim([0, 1.1])
    plt.title(f'Precision-Recall Curve Q{query} ({mode} mode)')
    plt.savefig(f'./q{query}/p-r-curve-{mode}.png')
    plt.close()

def compute_rcs(results: dict, query: int):
    for k, v in results.items():
        precision_recall(v, k, query)

def print_stats(stats: dict) -> None:
    for key, value in stats.items():
        print(f"{key}: {value}")

def evaluate(query: int, mode: str) -> None:

    results = getResults(query, mode)
    stats = {
        'query': f'q{query}',
        'mode': mode,
        f'P@{PRECISION_AT}': precision_at_k(results),
        'AvP': average_precision(results),
    }

    return [stats, results]

if __name__ == "__main__":

    # Milestone 2 - Global Evaluation
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'm2':

        stats = []
        results = {}
        for query in range(1, 5):
            for mode in MODES['m2']:
                output = evaluate(query, mode)
                stats.append(output[0])
                results[mode] = output[1]
            compute_rcs(results, query)

        output = {
            'Results per query and per mode': stats,
            'Global MAP': mean_average_precision(stats),
        }
        
        print(json.dumps(output, indent=2))

    # Milestone 3 - Global Evaluation
    elif len(sys.argv) == 2 and sys.argv[1].lower() == 'm3':

        stats = []
        results = {}
        for query in range(5, 9):
            for mode in MODES['m3']:
                output = evaluate(query, mode)
                stats.append(output[0])
                results[mode] = output[1]
            compute_rcs(results, query)

        output = {
            'Results per query and per mode': stats,
            'Global MAP': mean_average_precision(stats),
        }
        
        print(json.dumps(output, indent=2))

    # Milestone 2 - Single Evaluation (1, 2, 3, 4)
    elif len(sys.argv) == 2 and 1 <= int(sys.argv[1]) <= 4:

        stats = []
        results = {}
        for mode in MODES['m2']:
            output = evaluate(int(sys.argv[1]), mode)
            stats.append(output[0])
            results[mode] = output[1]
        compute_rcs(results, int(sys.argv[1]))

        print("Stats per query and per mode")
        print(json.dumps(stats, indent=2))

    # Milestone 3 - Single Evaluation (5, 6, 7, 8)
    elif len(sys.argv) == 2 and 5 <= int(sys.argv[1]) <= 8:

        stats = []
        results = {}
        for mode in MODES['m3']:
            output = evaluate(int(sys.argv[1]), mode)
            stats.append(output[0])
            results[mode] = output[1]
        compute_rcs(results, int(sys.argv[1]))

        print("Stats per query and per mode")
        print(json.dumps(stats, indent=2))

    else:
        print("Bad arguments. Usage:")
        print("   python3 evaluation.py M<2,3>          - for global milestone evaluation")
        print("   python3 evaluation.py <1, 2, 3, 4>    - for individual evaluation of milestone 2 queries")
        print("   python3 evaluation.py <5, 6, 7, 8>    - for individual evaluation of milestone 3 queries")