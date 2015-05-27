# coding: utf-8
from __future__ import unicode_literals, print_function
import codecs
from collections import defaultdict
import os
import re
import nltk
import time
from django.core.management.base import BaseCommand, CommandError
from unidecode import unidecode
from twitter.models import Tweet


STOPWORDS_PATH = os.path.join(os.path.dirname(__file__), 'stopwords.txt')
URL_PATTERN = re.compile(r'((www\.[^\s]+)|(https?://[^\s]+))')
USERNAME_PATTERN = re.compile(r'@[^\s]+', re.UNICODE)
WHITESPACE_PATTERN = re.compile(r'[\s]+', re.UNICODE)
HASHTAG_PATTERN = re.compile(r'#([^\s]+)', re.UNICODE)
WORD_PATTERN = re.compile(r'^\w[\w\d_]*$', re.UNICODE)
NUMBER_PATTERN = re.compile(r'\b[\d,.]+\b', re.UNICODE)


def process_tweet(tweet):
    # convert to lower case
    tweet = unidecode(tweet.lower())
    # convert www.* or https?://* to URL
    tweet = re.sub(URL_PATTERN, 'URL', tweet)
    # convert @username to AT_USER
    tweet = re.sub(USERNAME_PATTERN,'AT_USER',tweet)
    # remove additional white spaces
    tweet = re.sub(WHITESPACE_PATTERN, ' ', tweet)
    # replace #word with word
    tweet = re.sub(HASHTAG_PATTERN, r'\1', tweet)
    # remove numbers
    tweet = re.sub(NUMBER_PATTERN, '', tweet)
    tweet = tweet.strip('\'"')
    return tweet


def get_stopwords(filepath=STOPWORDS_PATH):
    stopwords = ['AT_USER', 'URL']
    with codecs.open(filepath, 'r', 'utf-8') as f:
        for line in f:
            stopwords.append(line.strip())
    return stopwords


def get_feature_vector(tweet, stopwords=get_stopwords()):
    feature_vector = []
    words = tweet.split()
    for word in words:
        word = word.strip('\'"\?,.!')
        if word not in stopwords and re.match(WORD_PATTERN, word):
            feature_vector.append(word.lower())
    return feature_vector


FEATURE_LIST = set()

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in FEATURE_LIST:
        features['contains(%s)' % word] = word in tweet_words
    return features


class Command(BaseCommand):
    def handle(self, *args, **options):
        tweets = []

        trains = Tweet.objects.filter(train=True).exclude(klass__isnull=True)
        if not trains:
            raise CommandError('No train data, please add some from the admin page!')

        for train in trains:
            sentiment = train.klass
            feature_vect = get_feature_vector(process_tweet(train.body))
            tweets.append((feature_vect, sentiment))
            FEATURE_LIST.update(feature_vect)

        training_set = nltk.classify.util.apply_features(extract_features, tweets)
        nb_classifier = nltk.NaiveBayesClassifier.train(training_set)

        while True:
            unclassified_tweets = Tweet.objects.filter(train=False, klass=None)
            total_count = unclassified_tweets.count()
            if total_count > 0:
                print('Processing %d tweets...' % total_count)
                counts = defaultdict(int)
                start_time = time.time()
                for tweet in unclassified_tweets:
                    feature_vect = get_feature_vector(process_tweet(tweet.body))
                    sentiment = nb_classifier.classify(extract_features(feature_vect))
                    counts[sentiment] += 1
                    tweet.klass = sentiment
                    msg = ['%d %s' % (counts[k], v) for k, v in Tweet.CLASSES]
                    print('\r' + ', '.join(msg), end='')
                    tweet.save()
                end_time = time.time()
                print('\nProcessing finished in %d seconds.' % int(end_time - start_time))
            print('Waiting...')
            time.sleep(3)