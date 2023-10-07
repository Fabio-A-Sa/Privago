import json
import pandas as pd
import numpy as np
from unidecode import unidecode
from utils import writeToFile, HOTELS_PATH, REVIEWS_PATH, HOTEL_REVIEWS_PATH
from data_analyze import tokenize_text

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
    hotels = pd.read_json(HOTELS_PATH)

    hotels_dict = {}
    for h in range(len(hotels)):
        hotels_dict[ hotels.loc[h, "name"] ] = 0 # number_of_reviews
    
    for r in range(len(hotel_reviews)):
        if hotel_reviews.loc[r, "name"] not in hotels_dict.keys():
            print(f'{hotel_reviews.loc[r, "name"]} not in the hotels list!') 
            continue

        hotels_dict[ hotel_reviews.loc[r, "name"] ] = hotels_dict[ hotel_reviews.loc[r, "name"] ] + 1

    reviews_per_hotel_dict = {
        "hotel": hotels_dict.keys(),
        "reviews": hotels_dict.values(),
    }
    writeToFile(HOTEL_REVIEWS_PATH, pd.DataFrame.from_dict(reviews_per_hotel_dict))

if __name__ == '__main__':
    hotels_average_rate()
    words_per_review()
    reviews_per_hotel()