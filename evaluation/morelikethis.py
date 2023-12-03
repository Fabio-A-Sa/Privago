import spacy
import json

nlp = spacy.load("en_core_web_sm")
RESULTS_PATH = "./mlt/results.json"

def calculate_similarity(review, similar_texts):
    doc1 = nlp(review)
    similarities = []

    for text in similar_texts:
        doc2 = nlp(text)
        similarity = doc1.similarity(doc2)
        similarities.append(similarity)

    return similarities

def print_results(entry, similarities):
    print(f"Review: {entry['review']}")
    print("Similarities:")

    for i, similarity in enumerate(similarities, 1):
        print(f"Result {i}: {similarity}")

    print("\n")

def main():
    with open(RESULTS_PATH, 'r') as file:
        results = json.load(file)

    for entry in results:
        review = entry['review']
        similar_texts = entry['semelhantes']
        similarities = calculate_similarity(review, similar_texts)

        print_results(entry, similarities)

if __name__ == "__main__":
    main()
