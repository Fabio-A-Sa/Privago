import json
import pandas as pd
import numpy as np
import re
from unidecode import unidecode
from utils import writeToFile, REVIEWS_PATH

def combine_reviews(row):
    if row['positive_review'] and row['negative_review']:
        return row['positive_review'] + '. ' + row['negative_review']
    elif row['positive_review']:
        return row['positive_review']
    elif row['negative_review']:
        return row['negative_review']
    else:
        return ''

def dealWithNullData(data_frame):
    
    for column in data_frame.columns:
        data_frame = data_frame[data_frame[column] != None]
        data_frame = data_frame[data_frame[column].notna()]
        data_frame = data_frame[data_frame[column] != "null"]
        data_frame = data_frame[data_frame[column] != np.nan]
        data_frame = data_frame[data_frame[column] != ""]
    
    if "review_text" in data_frame.columns:
        data_frame = data_frame[data_frame["review_text"] != " no comments available for this review"]
    return data_frame

def formatDate(data_frame: json, index: int):

    # Format 2016-11-07T00:00:00.000Z
    if index == 1: 
        data_frame['review_date'] = pd.to_datetime(data_frame['review_date'], format='mixed').dt.strftime("%Y-%m")

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

def formatName(data_frame: json):

    data_frame['name'] = data_frame['name'].apply(unidecode)
    data_frame['name'] = data_frame['name'].apply(lambda name: re.sub(r'[^\w\s]', '', name))
    data_frame['name'] = data_frame['name'].apply(lambda name: ' '.join(name.split()))
    data_frame['name'] = data_frame['name'].apply(lambda name: name.title())
    return data_frame


def limit_words_per_review(data_frame: json):
    
    data_frame['word_count'] = data_frame['review_text'].apply(lambda text: len(text.split()))
    description = data_frame['word_count'].describe()
    inferior_limit = description['25%']
    superior_limit = description['75%']
    data_frame = data_frame[(data_frame['word_count'] >= inferior_limit) & (data_frame['word_count'] <= superior_limit)]
    data_frame = data_frame.drop(['word_count'], axis=1)
    return data_frame

def normalize(index: int):

    file_path = f'../data/processed/hotel_reviews_{index}.json'
    data_frame = pd.read_json(file_path)

    # Remove empty and null entries
    data_frame = dealWithNullData(data_frame)

    # Combining positive and negative reviews
    if index == 4:
        for flavor in ["negative", "positive"]:
            data_frame[f'{flavor}_review'] = data_frame[f'{flavor}_review'].apply(lambda text: '' if text.lower() == f'no {flavor}' else text).str.strip()
        data_frame['review_text'] = data_frame.apply(combine_reviews, axis=1)
        data_frame.drop(['positive_review', 'negative_review'], axis=1, inplace=True)

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

    data_frame = limit_words_per_review(data_frame)

    data_frame = formatName(data_frame)

    # Save progress
    writeToFile(file_path, data_frame)



if __name__ == "__main__":
    for i in range(1, 5):
        normalize(i)