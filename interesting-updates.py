import manual_algorithm as ma
import nlp
import praw
import web_scraping
from newsapi import NewsApiClient
import requests
import os

def run():
    # 1. get interests
    interests = ma.get_top_interests()

    # 2. get reddit posts
    reddit = web_scraping.get_reddit()
    dirname = os.path.join('news')
    for i in interests:
        # print ("!!!!!!!!!" + i)
        filename = i + '.txt'
        web_scraping.get_top(i)
        desc = reddit.subreddit(i).description
        open(os.path.join(dirname, filename), 'a', encoding = 'utf-8').write(desc)

    # 3. run NLP
    top_keywords = []
    for i in interests:
        print("trimming " + i + ".txt")
        data_trimmed = nlp.pre_process('news/'+ i + '.txt')
        # print (i)
        top_words = nlp.get_top_words(data_trimmed)
        print (top_words)
        top2_words = nlp.get_top_n2_words(data_trimmed, n=20)
        print (top2_words)
        top_keywords.append(top2_words[0][0])
        top3_words = nlp.get_top_n3_words(data_trimmed, n=20)
        print (top3_words)

    #4. get news from interests
    newsapi = NewsApiClient(api_key='f208ccd69512466d9c1bb876566d4191')
    num = 1
    for cnt, keyword in enumerate(top_keywords):
        print (keyword)
        # os.makedirs('updates-for-you', exist_ok=True)
        top_headlines = newsapi.get_everything(q= keyword,
                                                sort_by='relevancy',
                                                language='en',
                                                page_size=2
                                                )
        count = 2
        num_art = 0
        for i in range(2):
            title = top_headlines['articles'][i]['title']
            url = top_headlines['articles'][i]['url']
            article = web_scraping.get_article(url)
            filename = "updates-for-you/article" + str(num) + ".txt"
            if article:
                num = num + 1
                with open(filename, 'w', encoding='utf-8') as file:
                    text = '\n\n'.join(article['content'])
                    file.write(text)

if __name__ == '__main__':
    run()
