import json
import requests
import pandas as pd
import ast
import os
from unidecode import unidecode

def getData() -> list:

    common = "https://opendata.porto.digital"
    next_endpoint = "/api/3/action/datastore_search?resource_id=35172eff-c68d-4162-93e5-528b95011584"
    data = []

    while True:

        url = common + next_endpoint
        response = requests.get(url)

        if response.status_code == 200:

            json_data = json.loads(response.text)
            items = json_data['result']['records']
            if len(items) != 0:
                data.extend(items)
            else:
                return data

            next_endpoint = json_data['result']['_links']['next']

        else:
            print("Failed to retrieve data from the URL. Status code: {}".format(response.status_code))
            return None

def processData(data: str) -> str:

    data_frame = pd.DataFrame(data)
    selected_attributes = ['_id', 'created', 'updated', 'latitude', 'longitude', 'data']

    data_frame['data'] = data_frame.apply(lambda row: getDescriptions(row['description'], row['label']), axis = 1)
    processed_data = data_frame[selected_attributes].rename(columns={'_id': 'id'}).to_dict(orient='records')

    return processed_data

def getDescriptions(descriptions_raw: str, labels_raw: str) -> list:

    descriptions = []
    descriptions_json = ast.literal_eval(descriptions_raw)
    labels_json = ast.literal_eval(labels_raw)
    
    for label in labels_json:
        lang = label['lang']
        description = [obj['value'] for obj in descriptions_json if obj.get('lang') == lang][0]
        item = {
            'lang': lang,
            'title': normalize(label['value']),
            'description': normalize(description)
        }
        descriptions.append(item)

    return descriptions

def normalize(text: str) -> str:
    return unidecode(text).replace('\"', "'")

def analyse_data(file_name):

    df = pd.read_json(file_name)

    df['word_count'] = df['data'].apply(lambda x: len(x[0]['description'].split()))
    print("\nMédia do número de palavras nas descrições:", round(df['word_count'].mean(), 1))

    print("\nNúmero de entidades:", df.shape[0])

def run():

    file_name = "processed_data.json"

    if not os.path.exists(file_name):
       
        raw_data = getData()
        with open("raw_data.json", "w") as file:
            file.write(json.dumps(raw_data, indent=2))
            file.close()

        processed_data = processData(raw_data)
        with open(file_name, "w") as file:
            file.write(json.dumps(processed_data, indent=2))
            file.close()

    analyse_data(file_name)

if __name__ == "__main__":
    run()