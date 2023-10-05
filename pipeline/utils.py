import json

def writeToFile(filename: str, data: json):
    with open(filename, 'w') as file:
        file.write(json.dumps(data.to_dict(orient='records'), indent=2))
        file.close()