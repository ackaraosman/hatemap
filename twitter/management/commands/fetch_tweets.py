# coding: utf-8
from __future__ import unicode_literals
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, Polygon, fromstr, GEOSGeometry
from twitter.models import Tweet
import tweepy


turkey_geojson = open(os.path.join(os.path.dirname(__file__), 'turkey.geojson')).read()
turkey = GEOSGeometry(turkey_geojson)


def contains_bad_word(text):
    # kelime gruplarinda sicti: got lalesi
    words = text.lower().split()
    for kelime in KELIMELER:
        if kelime in words:
            return True
    return False


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        coordinates = None
        save_tweet = False
        point = None

        if status.user.screen_name in ['hege_monya', 'hegemonya']:
            import ipdb; ipdb.set_trace()

        if hasattr(status, 'coordinates') and status.coordinates:
            coordinates = status.coordinates['coordinates']
            point = fromstr('POINT(%s %s)' % tuple(coordinates))
            if turkey.contains(point):
                if contains_bad_word(status.text):
                    save_tweet = True
        else:
            if contains_bad_word(status.text):
                point = fromstr('POINT(%s %s)' % status.place.bounding_box.origin())
                save_tweet = True

        if save_tweet:
            tweet = Tweet.objects.create(
                username=status.user.screen_name,
                body=status.text,
                point=point,
                place_name=status.place.name,
                place_full_name=status.place.full_name,
            )
            print(b'GOT ONE\x07')
        else:
            print("doesn't contain bad word")

        return True


consumer_token = 'F3re9ZTs0KfFajt0MM0x3rasb'
consumer_secret = 'gqjSUpx3JYViPumEK5AEvQSpHpLiO0ovmQWdEO2BjjFRszyYK1'

access_token = '8173792-okNKPBAFE6oBxoCxbQRXYqYZHbK34eiGyooW7NbJhK'
access_token_secret = '8BcpampuzJSBmo1zstHc2iw9igvCcaenMl0fpdODy7TMt'


homofobik = [
    'lezbiyen',
    'nonoş',
    'homoseksüel',
    'ipne',
    'ibne',
    'oğlancı',
]

irkci = [
    'ermeni köpeği',
    'ermeni dölü',
    'rum tohumu',
    'pis kürt',
    'sahtekar çerkez',
    'sahtekar çerkes',
    'alçak azeri',
    'hain arap',
    'gürcü domuzu',
    'terörist müslüman',
]

hakaret = [
    'pezevenk',
    'pezeveng',
    'gavat',
    'godoş',
    'dürzü',
    'at kafası',
    'göt lalesi',
    'yavşak',
    'yavsak',
    'piç',
    'göt',
    'orospu',
    'götveren',
    'göt veren',
    'amcık',
    'amın oğlu',
    'sik',
    'siktir',
    'puşt',
    'yarrak',
    'yarrrak',
    'yarram',
    'yarrram',
    'amk',
    'amına',
    'denyo',
]


KELIMELER = homofobik + irkci + hakaret


class Command(BaseCommand):
    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())
        myStream.filter(locations=[26.04,35.87,44.99,42.45])
        # myStream.filter(track=homofobik + irkci + hakaret)
