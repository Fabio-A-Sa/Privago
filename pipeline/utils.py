import json

HOTELS_PATH = '../data/processed/hotels.json'
REVIEWS_PATH = '../data/processed/reviews.json'
WORDS_PATH = '../data/analysis/words.json'
PLOTS_PATH = '../data/plots/'

def writeToFile(filename: str, data: json):
    with open(filename, 'w') as file:
        file.write(json.dumps(data.to_dict(orient='records'), indent=2))
        file.close()