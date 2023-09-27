import json
from tokenize import Double
import requests
import pandas as pd
import ast
import os

def writeToFile(filename: str, data: json):
    with open(filename, 'w') as file:
        file.write(json.dumps(data.to_dict(orient='records'), indent=2))
        file.close()

def printStats(dataset_index: int, processed_data: json):
    count = processed_data.groupby('name')['review_rate'].count()
    count_df = count.reset_index()
    count_df = count_df.rename(columns={'reviews': 'qtd'})

    writeToFile(f'../data/stats/hotel_reviews_{dataset_index}.json', count_df)
    print("{} - {} reviews - {} unique hotels".format(dataset_index, len(processed_data), processed_data['name'].nunique()))

def combine_reviews(row):
    if row['positive_review'] and row['negative_review']:
        return row['positive_review'] + '. ' + row['negative_review']
    elif row['positive_review']:
        return row['positive_review']
    elif row['negative_review']:
        return row['negative_review']
    else:
        return ''

def getData(dataset_index: int, attributes: dict):

    data_frame = pd.read_csv(f'../data/raw/hotel_reviews_{dataset_index}.csv', encoding='latin1')

    if dataset_index == 3:
        data_frame['location'] = 'London'

    data_frame = data_frame[attributes.keys()].rename(columns=attributes)

    if dataset_index == 4:

        for flavor in ["negative", "positive"]:
            data_frame[f'{flavor}_review'] = data_frame[f'{flavor}_review'].apply(lambda text: '' if text.lower() == f'no {flavor}' else text).str.strip()
        
        data_frame['review_text'] = data_frame.apply(combine_reviews, axis=1)
        data_frame.drop(['positive_review', 'negative_review'], axis=1, inplace=True)

    writeToFile(f'../data/processed/hotel_reviews_{dataset_index}.json', data_frame)
    printStats(dataset_index, data_frame)

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

    writeToFile(file_path, df)

def run():

    # Select important columns
    getData(1, {'name': 'name', 'city': 'location', 'reviews.date': 'review_date', 'reviews.text': 'review_text', 'reviews.rating': 'review_rate',})
    getData(2, {'Name': 'name', 'Area': 'location', 'Review_Date': 'review_date', 'Review_Text': 'review_text', 'Rating(Out of 10)': 'review_rate'})
    getData(3, {'Property Name': 'name', 'location': 'location', 'Date Of Review': 'review_date', 'Review Text': 'review_text', 'Review Rating': 'review_rate'})
    getData(4, {'Hotel_Name': 'name', 'Hotel_Address': 'location', 'Review_Date': 'review_date', 'Positive_Review': 'positive_review', 'Negative_Review': 'negative_review', 'Reviewer_Score': 'review_rate'})

    # Normalization
    for i in range(1, 5):
        normalization(i)

if __name__ == "__main__":
    run()