import json
import pandas as pd
from utils import writeToFile

def merge(indexes):   
    
    all_data = []
    for index in indexes:
        with open(f'../data/processed/hotel_reviews_{index}.json', 'r') as file:
            all_data.extend(json.load(file))
            file.close()

    writeToFile(f'../data/processed/hotel_reviews_all.json', pd.DataFrame(all_data))

if __name__ == '__main__':
    merge([x for x in range(1, 5)])