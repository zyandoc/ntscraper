import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import unquote, urlparse
from time import sleep
from base64 import b64decode
from random import uniform
from re import match, sub
from datetime import datetime
import logging
from logging.handlers import QueueHandler
from multiprocessing import Pool, Queue, cpu_count
from sys import stdout
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[QueueHandler(Queue()), logging.StreamHandler(stdout)]
)

class Nitter:
    def __init__(self):
        self.base_url = 'https://nitter.net'

    def get_tweets(self, keyword, mode='term', number=100):
        search_url = f"{self.base_url}/search?f=tweets&q={keyword}&src=typed_query"
        response = requests.get(search_url)
        if response.status_code == 200:
            tweets = self.parse_tweets(response.text, number)
            return {'tweets': tweets}
        else:
            return {'tweets': []}

    def parse_tweets(self, html, number):
        soup = BeautifulSoup(html, 'html.parser')
        tweets = [tweet.text for tweet in soup.find_all('p', class_='tweet-text')]
        return tweets[:number]

    def get_tweets_for_paper(self, paper_url, mode='term', number=100):
        keyword = self.extract_keyword_from_url(paper_url)
        tweets = self.get_tweets(keyword, mode=mode, number=number)
        return tweets['tweets']

    def extract_keyword_from_url(self, url):
        parsed_url = urlparse(url)
        path_segments = parsed_url.path.split('/')
        if 'articles' in path_segments:
            index = path_segments.index('articles')
            if index + 1 < len(path_segments):
                return path_segments[index + 1]
        return 'example_keyword'

nitter = Nitter()
paper_url = 'https://www.nature.com/articles/s41586-024-08449-y'
tweets = nitter.get_tweets_for_paper(paper_url, mode='term', number=100)
print(tweets)