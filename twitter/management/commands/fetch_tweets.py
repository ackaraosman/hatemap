# coding: utf-8
from __future__ import unicode_literals, print_function
from datetime import datetime
import os
import pytz
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, Polygon, fromstr, GEOSGeometry
import tweepy
from unidecode import unidecode
from twitter.models import Tweet
from ._badwords import BADWORDS, BADWORDS_NOASCIIFY


turkey_geojson = open(os.path.join(os.path.dirname(__file__), 'turkey.geojson')).read()
turkey = GEOSGeometry(turkey_geojson)


def check_for_badwords(text, badwords):
    words = text.split()
    for badword in badwords:
        if any(word.startswith(badword) for word in words):
            return True
        if len(badword.split()) > 1:
            if badword in text:
                return True
    return False


def contains_bad_word(text):
    text = text.lower()
    ascifiedtext = unidecode(text)
    if check_for_badwords(ascifiedtext, BADWORDS):
        return True
    return check_for_badwords(text, BADWORDS_NOASCIIFY)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        coordinates = None
        save_tweet = False
        point = None

        if hasattr(status, 'coordinates') and status.coordinates:
            coordinates = status.coordinates['coordinates']
            point = fromstr('POINT(%s %s)' % tuple(coordinates))
            if turkey.contains(point):
                if contains_bad_word(status.text):
                    save_tweet = True
        else:
            if contains_bad_word(status.text):
                coordinates = status.place.bounding_box.origin()
                # HACK: if its origin is Turkey, then dont save it
                if coordinates != (25.668509, 35.8084193):
                    # FIXME: origin is the wrong coordinate
                    point = fromstr('POINT(%s %s)' % coordinates)
                    save_tweet = True

        if save_tweet:
            timestamp = int(status.timestamp_ms) / 1000.0
            created_at = datetime.fromtimestamp(timestamp, tz=pytz.utc)
            tweet = Tweet.objects.create(
                username=status.user.screen_name,
                body=status.text,
                point=point,
                place_name=status.place.name,
                place_full_name=status.place.full_name,
                tweet_id=status.id_str,
                created_at=created_at,
            )
            print('GOT ONE', status.text[:25])
        else:
            print("doesn't contain bad word", status.text[:25])

        return True


TWITTER_TOKENS = [
    {
        'consumer_token':       'F3re9ZTs0KfFajt0MM0x3rasb',
        'consumer_secret':      'gqjSUpx3JYViPumEK5AEvQSpHpLiO0ovmQWdEO2BjjFRszyYK1',
        'access_token':         '8173792-okNKPBAFE6oBxoCxbQRXYqYZHbK34eiGyooW7NbJhK',
        'access_token_secret':  '8BcpampuzJSBmo1zstHc2iw9igvCcaenMl0fpdODy7TMt',
    },

    # {
    #     'consumer_token':       'oBraYlYOUvcM2RyGpD56tCPxA',
    #     'consumer_secret':      'qz6DKIdZvd9uTEd94cpqVuByIzdfG53ECXLxjWPEu7R8xsCh0i',
    #     'access_token':         '2361044455-vxOOTgzl0UH13gHD96QrYiDwTPI1ACF8rL038ha',
    #     'access_token_secret':  'HMYp4t3dEmL4Vyjwm0FKy5tqVGfgGvrnHVvATIG1w0poO',
    # },
]


def listen_streaming_api(cred):
    auth = tweepy.OAuthHandler(cred['consumer_token'], cred['consumer_secret'])
    auth.set_access_token(cred['access_token'], cred['access_token_secret'])
    listener = MyStreamListener()
    myStream = tweepy.Stream(auth=auth, listener=listener)
    myStream.filter(locations=[26.04,35.87,44.99,42.45])


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in TWITTER_TOKENS:
            listen_streaming_api(item)
