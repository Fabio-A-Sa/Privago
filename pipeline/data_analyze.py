import json
import pandas as pd
from utils import writeToFile, REVIEWS_PATH, WORDS_PATH, PLOTS_PATH, HOTELS_PATH, HOTEL_WORDS_PER_REVIEW_PATH, FINAL_JSON_PATH
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

def tokenize_text(text : str) -> list[str]:

    words = [] 
    stop_words = nltk.corpus.stopwords.words('english')
    my_sentences = sent_tokenize(text, "english")

    for sentence in my_sentences:

        # String normalization
        for ponctuation in ['.', ',', '<', '>']:
            sentence = sentence.replace(ponctuation, ' ')
        words_tokenized = word_tokenize(sentence, "english")

        # Filter stop words
        non_stop_words = [word for word in words_tokenized if word.lower() not in stop_words]
        words = words + non_stop_words
    
    return words

def word_segmentation():

    nltk.download('punkt')
    nltk.download('stopwords')

    words_in_reviews = {}
    data = pd.read_json(REVIEWS_PATH)

    for review_index in range(len(data)):

        mytext = data.loc[review_index, 'review_text']

        for word in tokenize_text(mytext):
            if word in words_in_reviews.keys():
                words_in_reviews[word] = words_in_reviews[word] + 1
            else:
                words_in_reviews[word] = 1

    words_in_reviews_dict = {
        "word": words_in_reviews.keys(),
        "count": words_in_reviews.values(),
    }

    writeToFile(WORDS_PATH, pd.DataFrame.from_dict(words_in_reviews_dict))

def word_cloud():

    word_segmentation()
    words = pd.read_json(WORDS_PATH)

    # Sort words frequency
    word_count = []
    for i in range(len(words)):
        word_count.append((words.loc[i, "word"], words.loc[i, "count"]))
    word_count.sort(key=lambda elem: elem[1], reverse=True)

    # Get WordCloud
    LIMIT = 200 
    subset = word_count[:LIMIT]
    wordcloud = WordCloud(width = 800, height = 800,
                          collocations = False,
                          background_color = 'white',
                          min_font_size = 10).generate(' '.join(map(lambda x: (x[0] + " ") * x[1], subset)))

    # WordCloud image
    fig = plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    fig.savefig(PLOTS_PATH + "reviews_wordcloud.png")

def location_distribution():

    hotels = pd.read_json(FINAL_JSON_PATH)
    location_counts = hotels['location'].value_counts()

    # 10 most common locations
    top_10_locations = location_counts.head(10)

    # Chart
    fig, ax = plt.subplots()
    ax.pie(top_10_locations, labels=top_10_locations.index, autopct='%1.1f%%', startangle=90, labeldistance=1.2)
    ax.axis('equal')
    ax.set_title('10 most common locations distribution', y=1.08)

    # Save progress
    fig.savefig(PLOTS_PATH + "location_distribution.png", bbox_inches='tight')

def rating_distribution():

    # Collect hotels average rating
    average_rates = []
    with open(FINAL_JSON_PATH, 'r') as file:
        average_rates = [hotel['average_rate'] for hotel in json.load(file)]
        file.close()

    # Histogram
    data_frame = pd.DataFrame({'average_rate': average_rates})
    plt.hist(data_frame['average_rate'], bins=range(6), edgecolor='k', alpha=0.7)
    plt.xlabel('Hotel average rate')
    plt.ylabel('Frequency')
    plt.xticks(range(6))

    # Save progress
    plt.savefig(PLOTS_PATH + "rating_distributions.png")

# TODO: Move this function. It is a subroutine of sample pipeline step.
def hotel_words_per_review():
    hotel_reviews = pd.read_json(REVIEWS_PATH)
    hotels = pd.read_json(HOTELS_PATH)

    hotels_dict = {}
    for h in range(len(hotels)):
        hotels_dict[ hotels.loc[h, "name"] ] = (0, 0) # (number_of_reviews, number_of_words)
    
    for r in range(len(hotel_reviews)):

        if hotel_reviews.loc[r, "name"] not in hotels_dict.keys():
            print(f'{hotel_reviews.loc[r, "name"]} not in the hotels list!') 
            continue

        hotels_dict[ hotel_reviews.loc[r, "name"] ] = (
            hotels_dict[ hotel_reviews.loc[r, "name"] ][0] + 1,
            hotels_dict[ hotel_reviews.loc[r, "name"] ][1] + len(tokenize_text(hotel_reviews.loc[r, "review_text"]))
        )
    
    hotels_words_per_review = {}
    
    for key in hotels_dict.keys():
        if hotels_dict[key] == 0:
            print(f'{key} has no reviews!')
            continue
        hotels_words_per_review[key] = round(hotels_dict[key][1] / hotels_dict[key][0], 2)

    hotels_words_per_review_dict = {
        "hotel": hotels_words_per_review.keys(),
        "words_per_review": hotels_words_per_review.values(),
    }

    writeToFile(HOTEL_WORDS_PER_REVIEW_PATH, pd.DataFrame.from_dict(hotels_words_per_review_dict))

if __name__ == '__main__':
    rating_distribution()
    location_distribution()
    word_cloud()
    # hotel_words_per_review() 