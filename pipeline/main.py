import json
import pandas as pd
import numpy as np
from datetime import datetime
from unidecode import unidecode
import matplotlib.pyplot as plt

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
        data_frame = data_frame[data_frame[column] != ""]
    return data_frame

def words_quantity(text: str):
    return len(text.split(' '))

def words(data_frame: json, index: int):
    data_frame['word_count'] = data_frame['review_text'].apply(lambda x: len(str(x).split()))
    
    # Step 4: Calculate the mean number of words
    mean_word_count = data_frame['word_count'].mean()

    # Step 5: Create a bar chart with a line representing the mean
    plt.figure(figsize=(10, 6))
    plt.bar(data_frame.index, data_frame['word_count'], label='Number of Words')
    plt.axhline(mean_word_count, color='red', linestyle='dashed', label='Mean Word Count')
    plt.text(0, mean_word_count, f'{mean_word_count:.2f}', color='red', va='center', ha='right')
    plt.xlabel('Review Index')
    plt.ylabel('Number of Words')
    plt.title('Number of Words in Hotel Reviews')
    # plt.ylim(0, 1000) # isto limita o y
    plt.legend()
    plt.savefig(f'../data/plots/word_count_{index}.png')

    return

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

def normalization(index: int):

    file_path = f'../data/processed/hotel_reviews_{index}.json'
    data_frame = pd.read_json(file_path)

    # Remove empty and null entries
    data_frame = dealWithNullData(data_frame)

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

    # Remove some reviews
    data_frame = data_frame[data_frame['review_text'].apply(lambda x: 10 <= len(x.split()) <= 250)]

    # Save progress
    writeToFile(file_path, data_frame)
    printStats(index, data_frame, True)

#def reviews_per_hotel(data_frame):
    #reviews_count = data_frame['name'].value_counts()
    #print(reviews_count)

def merge(indexes):   
    
    all_data = []
    for index in indexes:
        with open(f'../data/processed/hotel_reviews_{index}.json', 'r') as file:
            all_data.extend(json.load(file))
            file.close()

    writeToFile(f'../data/processed/hotel_reviews_all.json', pd.DataFrame(all_data))

def statistic(data_frame):
    average_ratings = data_frame.groupby('name')['review_rate'].mean().reset_index()
    writeToFile('../data/stats/hotel_reviews_all.json', average_ratings)    

def quartis(data_frame):

    data_frame['num_words'] = data_frame['review_text'].apply(lambda x: len(str(x).split(' ')))
    quartis = data_frame['num_words'].quantile([0.25, 0.5, 0.75])

    plt.figure(figsize=(8, 6))
    plt.boxplot(data_frame['num_words'], vert=False)
    plt.title('Quartiles Analysis of Number of Words per Review')
    plt.xlabel('Number of Words')
    plt.yticks([])

    quartis_labels = ['Q1', 'Q2 (Median)', 'Q3']
    quartis_values = [int(quartis[0.25]), int(quartis[0.5]), int(quartis[0.75]), int(quartis[0.1]), int(quartis[0.9])]
    
    print(quartis['0.9'])

    plt.xticks(quartis_values, quartis_labels)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.show()

def run():

    # Select important columns
    # getData(1, {'name': 'name', 'city': 'location', 'reviews.date': 'review_date', 'reviews.text': 'review_text', 'reviews.rating': 'review_rate',})
    # getData(2, {'Name': 'name', 'Area': 'location', 'Review_Date': 'review_date', 'Review_Text': 'review_text', 'Rating(Out of 10)': 'review_rate'})
    # getData(3, {'Property Name': 'name', 'location': 'location', 'Date Of Review': 'review_date', 'Review Text': 'review_text', 'Review Rating': 'review_rate'})
    # getData(4, {'Hotel_Name': 'name', 'Hotel_Address': 'location', 'Review_Date': 'review_date', 'Positive_Review': 'positive_review', 'Negative_Review': 'negative_review', 'Reviewer_Score': 'review_rate'})

    # Normalization
    # for i in range(1, 5):
    #   normalization(i)

    # Merge
    # merge([x for x in range (1, 5)])

    # Stats
    data_frame = pd.read_json('../data/processed/hotel_reviews_all.json')
    # statistic(data_frame)
    # words(data_frame)
    quartis(data_frame)

    # words(data_frame, 5)

if __name__ == "__main__":
    run()