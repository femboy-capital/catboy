import requests
import time
import random


class RedditFetcher:
    def __init__(self, subreddit, ttl=30.0):
        self.subreddit = subreddit
        self.ttl = ttl
        self.last_fetched = time.monotonic() - ttl # just a hack to init lol
        self.cache = None

    def fetch_random(self, posted_cache):
        if self.last_fetched + self.ttl < time.monotonic():
            r = requests.get(url='https://www.reddit.com/r/{0}/top.json?limit=20&t=day'.format(self.subreddit), headers={'User-agent': 'Catboy 0.1'})
            posts = r.json()
            if 'data' in posts:
                self.cache = posts
            self.last_fetched = time.monotonic()

        tried = 0
        while tried < len(self.cache['data']['children']):
            post = random.choice(self.cache['data']['children'])
            if not post['data']['url'] in posted_cache:
                return post['data']['url']
            tried += 1
        
        return None
