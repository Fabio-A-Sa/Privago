import json
import pandas as pd
import numpy as np
from unidecode import unidecode
from utils import writeToFile, HOTELS_PATH, REVIEWS_PATH

def hotels_average_rate():

    hotel_reviews = pd.read_json(REVIEWS_PATH)
    grouped_reviews_rate = hotel_reviews.groupby('name').agg({'review_rate': 'mean', 'location': 'first'}).reset_index().round(2)
    grouped_reviews_rate.rename(
        columns={'review_rate': 'average_rate'}, inplace=True
    )

    writeToFile(HOTELS_PATH, grouped_reviews_rate)

def words_per_review():
    hotel_reviews = pd.read_json(REVIEWS_PATH)
    # TODO
    writeToFile(REVIEWS_PATH, hotel_reviews)

def reviews_per_hotel():
    hotel_reviews = pd.read_json(REVIEWS_PATH)
    # TODO
    writeToFile(REVIEWS_PATH, hotel_reviews)

if __name__ == '__main__':
    hotels_average_rate()
    words_per_review()
    reviews_per_hotel()