import spacy
import json

NPL = spacy.load("en_core_web_sm")
SOLR_RESULTS_PATH = "./mlt/results.json"
SOLR_EVALUATION_PATH = './mlt/evaluation.json'

def calculate_similarity(review, similar_texts):
    doc1 = NPL(review)
    similarities = []

    for text in similar_texts:
        doc2 = NPL(text)
        similarity = round(doc1.similarity(doc2), 3)
        similarities.append(similarity)

    return similarities

def save_evaluation(evaluation):
    
    a = []
    for (review, similiarities) in evaluation:
        b = round(sum(similiarities) / len(similiarities), 2)
        print(f"Partial: {b}")
        a.append(b)

    print(f"Total: {round(sum(a) / len(a), 2)}")

def main():

    # Get solr results
    results = []
    with open(SOLR_RESULTS_PATH, 'r') as file:
        results = json.load(file)
        file.close()

    # Evaluation based on similiarity
    evaluation = []
    for entry in results:
        review = entry['review']
        similar_texts = entry['related']
        similarities = calculate_similarity(review, similar_texts)
        evaluation.append([review, similarities])

    # Save progress
    save_evaluation(evaluation)

if __name__ == "__main__":
    main()
