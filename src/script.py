import json
import requests
import pandas as pd
import ast
import os

def processData(index: int, attributes: dict):

    data_frame = pd.read_csv(f'../data/raw/hotel_reviews_{index}.csv', encoding='latin1')

    if index == 3:
        data_frame['location'] = 'London'

    processed_data = data_frame[attributes.keys()].rename(columns=attributes).to_dict(orient='records')

    with open(f'../data/processed/hotel_reviews_{index}.json', 'w') as file:
        file.write(json.dumps(processed_data, indent=2))
        file.close()

def run():

    processData(1, {'name': 'name', 'city': 'location', 'reviews.date': 'review_date', 'reviews.text': 'review_text', 'reviews.rating': 'review_rate',})
    processData(2, {'Name': 'name', 'Area': 'location', 'Review_Date': 'review_date', 'Review_Text': 'review_text', 'Rating(Out of 10)': 'review_rate'})
    processData(3, {'Property Name': 'name', 'location': 'location', 'Date Of Review': 'reviews_date', 'Review Text': 'review_text', 'Review Rating': 'reviews_rate'})

if __name__ == "__main__":
    run()