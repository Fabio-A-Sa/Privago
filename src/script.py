import json
from tokenize import Double
import requests
import pandas as pd
import ast
import os

def getData(index: int, attributes: dict):

    data_frame = pd.read_csv(f'../data/raw/hotel_reviews_{index}.csv', encoding='latin1')

    if index == 3:
        data_frame['location'] = 'London'

    processed_data = data_frame[attributes.keys()].rename(columns=attributes)
    #print("{} - {} reviews - {} unique hotels".format(index, len(processed_data), processed_data['name'].nunique()))

    data_frame = dealWithNullData(index, data_frame)

    if index == 4:
        processed_data['review_text'] = processed_data['positive_review'] + '.' + processed_data['negative_review']
        processed_data.drop(['positive_review', 'negative_review'], axis=1, inplace=True)

    print("{} - {} reviews - {} unique hotels".format(index, len(processed_data), processed_data['name'].nunique()))
    with open(f'../data/processed/hotel_reviews_{index}.json', 'w') as file:
        file.write(json.dumps(processed_data.to_dict(orient='records'), indent=2))
        file.close()

    # Stats
    count = processed_data.groupby('name')['review_rate'].count()
    count_df = count.reset_index()
    count_df = count_df.rename(columns={'reviews': 'qtd'})

    with open(f'../data/stats/hotel_reviews_{index}.json', 'w') as file:
        file.write(json.dumps(count_df.to_dict(orient='records'), indent=2))
        file.close()

def dealWithNullData(index, df):
    df = df.replace(' Null', None)
   # df = df.replace('Null', null)
    df = df.dropna()

    # TODO: index 4 - remove strings "No Negative" and "No positive"
    return df

def normalization(index):

    file_path = f'../data/processed/hotel_reviews_{index}.json'
    df = pd.read_json(file_path)

    # Rate normalization
    if index in [2, 4]:
        df['review_rate'] = round(df['review_rate'] / 2, 1)
    df['review_rate'] = df['review_rate'].apply(float)
    
    # Date normalization
    # TODO

    # Drop if words(review_text) < 100 ?

    with open(file_path, 'w') as file:
        file.write(json.dumps(df.to_dict(orient='records'), indent=2))
        file.close()

def run():

    getData(1, {'name': 'name', 'city': 'location', 'reviews.date': 'review_date', 'reviews.text': 'review_text', 'reviews.rating': 'review_rate',})
    getData(2, {'Name': 'name', 'Area': 'location', 'Review_Date': 'review_date', 'Review_Text': 'review_text', 'Rating(Out of 10)': 'review_rate'})
    getData(3, {'Property Name': 'name', 'location': 'location', 'Date Of Review': 'review_date', 'Review Text': 'review_text', 'Review Rating': 'review_rate'})
    getData(4, {'Hotel_Name': 'name', 'Hotel_Address': 'location', 'Review_Date': 'review_date', 'Positive_Review': 'positive_review', 'Negative_Review': 'negative_review', 'Reviewer_Score': 'review_rate'})

    for i in range(1, 5):
        normalization(i)

if __name__ == "__main__":
    run()