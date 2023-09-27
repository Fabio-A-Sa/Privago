import json
import pandas as pd
import numpy as np
from datetime import datetime
from unidecode import unidecode

def writeToFile(filename: str, data: json):
    with open(filename, 'w') as file:
        file.write(json.dumps(data.to_dict(orient='records'), indent=2))
        file.close()

def printStats(dataset_index: int, processed_data: json, save: bool):

    if save:
        count = processed_data.groupby('name')['review_rate'].count()
        count_df = count.reset_index()
        count_df = count_df.rename(columns={'review_rate': 'qtd_reviews', 'name': 'hotel_name'})
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

    # Set location column
    if dataset_index == 3:
        data_frame['location'] = 'London'

    # Drop unnecessary columns
    data_frame = data_frame[attributes.keys()].rename(columns=attributes)

    # Combining positive and negative reviews
    if dataset_index == 4:
        for flavor in ["negative", "positive"]:
            data_frame[f'{flavor}_review'] = data_frame[f'{flavor}_review'].apply(lambda text: '' if text.lower() == f'no {flavor}' else text).str.strip()
        data_frame['review_text'] = data_frame.apply(combine_reviews, axis=1)
        data_frame.drop(['positive_review', 'negative_review'], axis=1, inplace=True)

    # Save progress
    writeToFile(f'../data/processed/hotel_reviews_{dataset_index}.json', data_frame)
    printStats(dataset_index, data_frame, False)

def dealWithNullData(data_frame):
    for column in data_frame.columns:
        data_frame = data_frame[data_frame[column] != None]
        data_frame = data_frame[data_frame[column].notna()]
        data_frame = data_frame[data_frame[column] != "null"]
        data_frame = data_frame[data_frame[column] != np.nan]
    return data_frame

def words(text: str):
    return len(text.split(' '))

def formatDate(data_frame: json, index: int):

    # Format 2016-11-07T00:00:00.000Z
    if index == 1: 
        data_frame['review_date'] = pd.to_datetime(data_frame['review_date']).dt.strftime("%Y-%m")

    # Format Jun-23
    if index == 2: 
        months = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        data_frame['review_date'] = data_frame['review_date'].str.split('-').apply(lambda x: f"20{x[1]}-{months[x[0]]}")

    # Format 04/30/2016
    if index in [3, 4]:
        data_frame['review_date'] = pd.to_datetime(data_frame['review_date'], format='%m/%d/%Y').dt.strftime("%Y-%m")

    return data_frame

def formatText(text: str):
    return unidecode(text).replace('\n', '').replace('\"', "'")

def normalization(index: int, n_words: int):

    file_path = f'../data/processed/hotel_reviews_{index}.json'
    data_frame = pd.read_json(file_path)

    # Remove empty and null entries
    data_frame = dealWithNullData(data_frame)

    # Remove reviews with less than @words
    data_frame = data_frame[data_frame['review_text'].apply(words) >= n_words]

    # Strings strip
    data_frame = data_frame.map(lambda column: column.strip() if isinstance(column, str) else column)

    # String format
    data_frame = data_frame.map(lambda text: formatText(text) if isinstance(text, str) else text)

    # Rate normalization [0.0 .. 5.0]
    if index in [2, 4]:
        data_frame['review_rate'] = round(data_frame['review_rate'] / 2, 1)
    data_frame['review_rate'] = data_frame['review_rate'].apply(float)
    
    # Date normalization
    data_frame = formatDate(data_frame, index)

    # Save progress
    writeToFile(file_path, data_frame)
    printStats(index, data_frame, True)

def run():

    # Select important columns
    getData(1, {'name': 'name', 'city': 'location', 'reviews.date': 'review_date', 'reviews.text': 'review_text', 'reviews.rating': 'review_rate',})
    getData(2, {'Name': 'name', 'Area': 'location', 'Review_Date': 'review_date', 'Review_Text': 'review_text', 'Rating(Out of 10)': 'review_rate'})
    getData(3, {'Property Name': 'name', 'location': 'location', 'Date Of Review': 'review_date', 'Review Text': 'review_text', 'Review Rating': 'review_rate'})
    getData(4, {'Hotel_Name': 'name', 'Hotel_Address': 'location', 'Review_Date': 'review_date', 'Positive_Review': 'positive_review', 'Negative_Review': 'negative_review', 'Reviewer_Score': 'review_rate'})

    # Normalization
    for i in range(1, 5):
        normalization(i, 100)

    # Get samples & merge
    # TODO

if __name__ == "__main__":
    run()