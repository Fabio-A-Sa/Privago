import pandas as pd
import nltk
from nltk import download
from nltk.corpus import wordnet


nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

file_path = f'../data/processed/hotels_complete.json'
dataset = pd.read_json(file_path)

all_texts = [review['text'] for reviews_list in dataset['reviews'] for review in reviews_list]

#print(all_texts)

word_dict = {}
words_checked = set()

for desc in all_texts:
    if not isinstance(desc, str):
        continue

    words = nltk.word_tokenize(desc)
    nouns = [word.lower() for word, pos in nltk.pos_tag(words) if pos in ['NN', 'NNS'] and word.lower() not in words_checked]

    for noun in nouns:
        synonyms = []
        for syn in wordnet.synsets(noun):
            for lm in syn.lemmas():
                if lm.name().lower() != noun:
                    synonyms.append(lm.name())  # adding into synonyms
        if len(synonyms) > 1:
            word_dict[noun] = set(synonyms)
            words_checked.add(noun)

with open("synonyms.txt", 'w') as f:
    for k, v in word_dict.items():
        matches = list(v - {k})  # Exclude the original word from synonyms
        list_synonyms = k + ", " + ", ".join(matches)
        f.write(list_synonyms + "\n")