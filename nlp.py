import pandas as pd
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

def pre_process(txt_file):
    with open(txt_file, encoding="utf8") as file:
        data = file.read().replace('\n', '')
    # print (data)

    ##Creating a list of stop words and adding custom stopwords
    stop_words = set(stopwords.words("english"))
    ##Creating a list of custom stopwords
    # new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown"]
    new_words = ["video", "unavailable", "youtube", "loading", "queueloading", "premium",
        "working", "watch", "queue", "http", "bit", "ly", "twitter", "www", "github",
        "io", "com", "reddit", "welcome", "discuss"]
    stop_words = stop_words.union(new_words)

    data_trimmed = []
    for i in range(10):
        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ', data)
        #Convert to lowercase
        text = text.lower()
        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
        ##Convert to list from string
        text = text.split()
        ##Stemming
        ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in
                stop_words]
        text = " ".join(text)
        data_trimmed.append(text)
    # print (data_trimmed)
    return data_trimmed

def get_top_words(data_trimmed):
    stop_words = set(stopwords.words("english"))
    cv = CountVectorizer(stop_words=stop_words, ngram_range=(1,3))
    X = cv.fit_transform(data_trimmed)
    return (list(cv.vocabulary_.keys())[:10])

def get_top_n2_words(data_trimmed, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2),
            max_features=2000).fit(data_trimmed)
    bag_of_words = vec1.transform(data_trimmed)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1],
                reverse=True)
    return words_freq[:n]

def get_top_n3_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(3,3),
           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1],
                reverse=True)
    return words_freq[:n]

if __name__ == '__main__':
    txt_file = 'txt-files/sample_reddit.txt'
    data_trimmed = pre_process(txt_file)
    get_top_words(data_trimmed)
    top2_words = get_top_n2_words(data_trimmed, n=20)
    print (top2_words)
    top3_words = get_top_n3_words(data_trimmed, n=20)
    print (top3_words)
