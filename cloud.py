#!/usr/bin/env python3

import os
import re
import json
import twitter
import requests
import argparse
from wordcloud import WordCloud
from bs4 import BeautifulSoup


class TwitterClient:
    def __init__(self):
        self.keys = json.loads(open('SECRETS.json').read())
        self.api = twitter.Api(
            consumer_key=self.keys['consumer_key'],
            consumer_secret=self.keys['consumer_secret'],
            access_token_key=self.keys['access_token'],
            access_token_secret=self.keys['access_token_secret'])

    def post(self, text, image):
        status = self.api.PostUpdate(text, media=image,
                                     verify_status_length=False)
        return status

boring_words = re.compile(r'\b(' + r'|'.join(
    open('boring_words.txt').read().split()
) + r')\b\s*')


def get(url):
    if not url.startswith('http'):
        url = 'http://' + url
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('no soup from "%s"' % url)

    text = r.text
    if r.encoding.lower() != 'utf-8':
        text = text.decode(r.encoding).encode('utf-8')

    return BeautifulSoup(text, 'html.parser')


def parse_soup(soup):
    super_text = []
    articles = soup.select(
        'article,.article,.article-content,.df-article-content'
    )
    for article in articles:
        lines = article.get_text().split('\n')
        text = ' '.join(lines).strip().lower()
        super_text.append(text)
    return '\n'.join(super_text)


class Cloud:
    def __init__(self, url, width=1200, height=600):
        self.url = url
        soup = get(url)
        text = parse_soup(soup)
        text = boring_words.sub('', text)
        if not text:
            raise Exception('invalid page format at "%s"' % url)
        self.cloud = WordCloud(width=width, height=height).generate(text)
        self.path = 'images'
        self.filename = url + '.png'

    def save(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.cloud.to_file(os.path.join(self.path, self.filename))


def main(args):
    client = TwitterClient()
    urls = args['url']
    for url in urls:
        cloud = Cloud(url)
        cloud.save()
        if args['tweet']:
            text = 'Dagens ordsky fra ' + url
            image = os.path.join(cloud.path, cloud.filename)
            client.post(text, image)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, nargs='+',
                        help='url of site to search for words; example: vg.no')
    parser.add_argument('--tweet', action='store_true')

    return vars(parser.parse_args())

if __name__ == '__main__':
    args = parse_args()
    main(args)
