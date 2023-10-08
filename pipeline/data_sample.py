import json
import pandas as pd
import numpy as np
import math
import random
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

# eliminar reviews
def purge_reviews(max_reviews_number: int):
    hotels_reviews = pd.read_json(HOTEL_REVIEWS_PATH)
    reviews = pd.read_json(REVIEWS_PATH)

    hotels_to_purge = []

    for i in range(len(hotels_reviews)):
        if (hotels_reviews.loc[i, "reviews"] > max_reviews_number):
            hotels_to_purge.append(hotels_reviews.loc[i, "hotel"])


    for hotel_to_purge in hotels_to_purge:
        reviews_to_purge = reviews.loc[reviews["name"] == hotel_to_purge]

        review_rates = {}
        for r in reviews_to_purge.index.tolist():
            if (reviews_to_purge.loc[r, "review_rate"] in review_rates.keys()):
                review_rates[ reviews_to_purge.loc[r, "review_rate"] ] = review_rates[ reviews_to_purge.loc[r, "review_rate"] ] + 1
            else:
                review_rates[ reviews_to_purge.loc[r, "review_rate"] ] = 1
            
        
        # deciding how many reviews in each rate are going to be deleetd

        result = [math.floor((rev/len(reviews_to_purge)) * max_reviews_number) for rev in review_rates.values()]
        result_rest = [(rev/len(reviews_to_purge)) * max_reviews_number - math.floor((rev/len(reviews_to_purge)) * max_reviews_number) for rev in review_rates.values()]
        
        idx_added = []
        for i in range(max_reviews_number - sum(result)):
            highest = -1
            for j in range(len(result)):
                if highest < 0:
                    if j in idx_added:
                        continue
                    else:
                        highest = j
                if (result_rest[highest] < result_rest[j] and j not in idx_added):
                    highest = j
            
            idx_added.append(highest)
        
        for idx in idx_added:
            result[idx] = result[idx] + 1

        # deleting reviews
        new_review_rates = {}

        for i in range(len(review_rates.keys())):
            new_review_rates[list(review_rates.keys())[i]] = result[i]
        
        for key in review_rates:
            diff = review_rates[key] - new_review_rates[key]
            if not diff: continue

            # choose which rows to drop
            idxs_to_purge = reviews_to_purge[reviews_to_purge["review_rate"] == key]
            idxs_to_purge = random.sample(idxs_to_purge.index.tolist(), diff)

            # drop the choosen rows
            reviews = reviews.drop(index=idxs_to_purge)
        
    
    writeToFile(REVIEWS_PATH, reviews)




if __name__ == '__main__':
    hotels_average_rate()
    words_per_review()
    reviews_per_hotel()
    purge_reviews(75)