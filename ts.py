import tweepy
from geopy.geocoders import Nominatim

geolocator = Nominatim()


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if hasattr(status, 'coordinates') and status.coordinates:
            coordinates = status.coordinates['coordinates']
            location = geolocator.reverse(','.join(str(f) for f in reversed(coordinates)))
            print 'from', location.address, '\n', status.text, '\n\n'
        else:
            print 'null coordinates\n', status.text, '\n\n'
        return True


consumer_token = 'F3re9ZTs0KfFajt0MM0x3rasb'
consumer_secret = 'gqjSUpx3JYViPumEK5AEvQSpHpLiO0ovmQWdEO2BjjFRszyYK1'

access_token = '8173792-okNKPBAFE6oBxoCxbQRXYqYZHbK34eiGyooW7NbJhK'
access_token_secret = '8BcpampuzJSBmo1zstHc2iw9igvCcaenMl0fpdODy7TMt'

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())
# myStream.filter(locations=[26.04,35.87,44.99,42.45])
myStream.filter(track=['ipne', 'ibne', 'sik'])
