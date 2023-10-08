import json
import pandas as pd
import numpy as np
from unidecode import unidecode
from utils import writeToFile, HOTELS_PATH, REVIEWS_PATH, HOTEL_REVIEWS_PATH, FINAL_JSON_PATH
from data_analyze import tokenize_text

def hotels_average_rate():

    hotel_reviews = pd.read_json(REVIEWS_PATH)
    grouped_reviews_rate = hotel_reviews.groupby('name').agg({'review_rate': 'mean', 'location': 'first'}).reset_index().round(2)
    grouped_reviews_rate.rename(
        columns={'review_rate': 'average_rate'}, inplace=True
    )

    writeToFile(HOTELS_PATH, grouped_reviews_rate)


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
    description = pd.DataFrame.from_dict(reviews_per_hotel_dict)["reviews"].describe()
    writeToFile(HOTEL_REVIEWS_PATH, pd.DataFrame.from_dict(reviews_per_hotel_dict))
    return(description['25%'], description['75%'])


def limit_hotel_reviews(inferior_limit: int, superior_limit: int):
    hotel_reviews = pd.read_json(HOTEL_REVIEWS_PATH)
    hotel_reviews = hotel_reviews[(hotel_reviews['reviews'] >= inferior_limit)]
    writeToFile(HOTEL_REVIEWS_PATH, pd.DataFrame.from_dict(hotel_reviews))

def final_json():
    reviews_per_hotel = pd.read_json(HOTEL_REVIEWS_PATH)
    hotels = pd.read_json(HOTELS_PATH)
    reviews = pd.read_json(REVIEWS_PATH)
    
    hotels_info = []
    for index, review_per_hotel in reviews_per_hotel.iterrows():
        hotel_name = review_per_hotel['hotel']
        hotel_info = hotels[hotels['name'] == hotel_name].to_dict(orient='records')[0]
        hotels_info.append({
            'name': hotel_info['name'],
            'location': hotel_info['location'],
            'average_rate': hotel_info['average_rate'],
            'reviews': []
        })

    for index, review in reviews.iterrows():
        hotel_name = review['name']
        for a in hotels_info:
            if hotel_name == a['name']:
                a['reviews'].append({
                    'date': review['review_date'],
                    'rate': review['review_rate'],
                    'text': review['review_text'],
                })

    writeToFile(FINAL_JSON_PATH, pd.DataFrame.from_dict(hotels_info))
    
if __name__ == '__main__':
    hotels_average_rate()
    limits = reviews_per_hotel()
    limit_hotel_reviews(limits[0], limits[1])
    final_json()