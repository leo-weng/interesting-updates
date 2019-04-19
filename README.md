# Interesting Updates

Interesting Updates is an infrastructure for personal news update delivery.

## Installation

Download the dataset from [Kaggle](https://www.kaggle.com/c/yandex-personalized-web-search-challenge/data). Note that the dataset is extremely large when uncompressed.


Install the following packages:

For SQLite3.
```bash
pip install sqlite3
```

For Reddit and web scraping. You will need to register for a Reddit API [here](https://www.reddit.com/wiki/api).

```bash
pip install praw
pip install beautifulsoup4
```

For ML algorithms:
```bash
pip install numpy
pip install scikit-learn
```

For NLP:
```bash
pip install re2
pip install nltk
```

For News. You will need to get an API key from [NewsAPI](https://newsapi.org/).

```bash
pip install newsapi-python
```

## Usage

```bash
# Create database, load table and insert data
python load_data.py
python load_data_subreddits.py

# Run interesting updates!
python interesting-updates.py

# If you can set up a cron job to run this in a background and give you updates periodically then that's dope.
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
