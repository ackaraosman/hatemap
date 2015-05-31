# coding: utf-8
from __future__ import unicode_literals, print_function
import codecs
from collections import defaultdict
import os
import re
import nltk
import time
from django import db
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from unidecode import unidecode
from twitter.models import Tweet
from ._badwords import BADWORDS, BADWORDS_NOASCIIFY


# In order to find first longest matched badword in get_feature_vector
# Sort BADWORDSs by their length in descencing order

BADWORDS = sorted(BADWORDS, key=len, reverse=True)
BADWORDS_NOASCIIFY = sorted(BADWORDS_NOASCIIFY, key=len, reverse=True)


STOPWORDS_PATH = os.path.join(os.path.dirname(__file__), 'stopwords.txt')
URL_PATTERN = re.compile(r'((www\.[^\s]+)|(https?://[^\s]+))')
USERNAME_PATTERN = re.compile(r'@[^\s]+', re.UNICODE)
WHITESPACE_PATTERN = re.compile(r'[\s]+', re.UNICODE)
HASHTAG_PATTERN = re.compile(r'#([^\s]+)', re.UNICODE)
WORD_PATTERN = re.compile(r'^\w[\w\d_]*$', re.UNICODE)
NUMBER_PATTERN = re.compile(r'\b[\d,.]+\b', re.UNICODE)


def process_tweet(tweet):
    # convert to lower case
    tweet = tweet.lower()
    # convert www.* or https?://* to URL
    tweet = re.sub(URL_PATTERN, 'URL', tweet)
    # convert @username to AT_USER
    tweet = re.sub(USERNAME_PATTERN,'AT_USER',tweet)
    # remove additional white spaces
    tweet = re.sub(r'[\'"\?,.!:;()]', ' ', tweet)
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


def which_badword(word, badwords):
    for badword in badwords:
        if word.startswith(badword):
            return badword
    return None


# get_feature_vector function tries to save CPU cycles as much as possible, if
# a word is not a stopword, instead of directly adding to feature_vector, first
# checks if it's a badword, then adds badword to feature_vector, otherwise adds
# the word itself. Since it iterates on badwords linearly, it adds the longest
# matched badword (BADWORDSs are sorted).

def get_feature_vector(tweet, stopwords=get_stopwords()):
    feature_vector = []
    words = tweet.split()
    for word in words:
        word = word.strip('\'"\?,.!')
        if word not in stopwords and re.match(WORD_PATTERN, word):
            badword = which_badword(word, BADWORDS_NOASCIIFY)
            if badword:
                feature_vector.append(badword)
            else:
                ascified = unidecode(word)
                badword = which_badword(word, BADWORDS_NOASCIIFY)
                if badword:
                    feature_vector.append(badword)
                else:
                    feature_vector.append(word.lower())
    return feature_vector


FEATURE_LIST = set()

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in FEATURE_LIST:
        features['contains(%s)' % word] = word in tweet_words
    return features


def get_classifier(trains):
    global FEATURE_LIST
    FEATURE_LIST = set()

    tweets = []
    for train in trains:
        sentiment = train.klass
        feature_vect = get_feature_vector(process_tweet(train.body))
        tweets.append((feature_vect, sentiment))
        FEATURE_LIST.update(feature_vect)

    training_set = nltk.classify.util.apply_features(extract_features, tweets)
    nb_classifier = nltk.NaiveBayesClassifier.train(training_set)
    return nb_classifier


def get_train_tweets():
    return Tweet.objects.filter(train=True).exclude(klass__isnull=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        trains = get_train_tweets()
        if not trains:
            raise CommandError('No train data, please add some from the admin page!')

        train_count = trains.count()
        classifier = get_classifier(trains)

        while True:
            unclassified_tweets = Tweet.objects.filter(train=False, klass=None)
            total_count = unclassified_tweets.count()
            if total_count > 0:
                print('Classifying %d tweets...' % total_count)
                counts = defaultdict(int)
                start_time = time.time()
                for tweet in unclassified_tweets:
                    feature_vect = get_feature_vector(process_tweet(tweet.body))
                    sentiment = classifier.classify(extract_features(feature_vect))
                    counts[sentiment] += 1
                    tweet.klass = sentiment
                    msg = ['%d %s' % (counts[k], v) for k, v in Tweet.CLASSES]
                    print('\r' + ', '.join(msg), end='')
                    tweet.save()
                    if settings.DEBUG:
                        db.reset_queries()
                elapsed = int(time.time() - start_time)
                print('\nClassifying finished in %d seconds.' % elapsed)

            new_trains = get_train_tweets()
            if new_trains.count() != train_count:
                print('Train set has been changed, retraining...')
                trains = new_trains
                train_count = new_trains.count()
                classifier = get_classifier(trains)
            else:
                print('Waiting...')
                time.sleep(3)
