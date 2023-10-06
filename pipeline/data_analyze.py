import pandas as pd
from utils import writeToFile, REVIEWS_PATH, WORDS_PATH, PLOTS_PATH, HOTELS_PATH
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

def word_segmentation():
    
    nltk.download('punkt')
    nltk.download('stopwords')

    words_in_reviews = {}
    stop_words = nltk.corpus.stopwords.words('english')
    data = pd.read_json(REVIEWS_PATH)

    for review_index in range(len(data)):

        mytext = data.loc[review_index, 'review_text']
        my_sentences = sent_tokenize(mytext, "english")

        for sentence in my_sentences:

            # String normalization
            for ponctuation in ['.', ',', '<', '>']:
                sentence = sentence.replace(ponctuation, ' ')
            words = word_tokenize(sentence, "english")

            # Filter stop words
            non_stop_words = [word for word in words if word.lower() not in stop_words]

            # Accumulate results
            for word in non_stop_words:
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
    fig.savefig(PLOTS_PATH + "wordcloud.png")

def location_chart():

    hotels = pd.read_json(HOTELS_PATH)
    location_counts = hotels['location'].value_counts()

    # 20 most common locations
    top_20_locations = location_counts.head(20)
    other_count = location_counts.iloc[20:].sum()
    top_20_locations['Other'] = other_count

    # Donuts chart
    fig, ax = plt.subplots()
    ax.pie(top_20_locations, labels=top_20_locations.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(circle)

    # Save plot
    fig.savefig(PLOTS_PATH + "locations.png")

if __name__ == '__main__':
    word_cloud()
    location_chart()