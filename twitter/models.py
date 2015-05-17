from django.contrib.gis.db import models


class Tweet(models.Model):
    username = models.CharField(max_length=20)
    body = models.TextField()
    point = models.PointField(null=True, blank=True)
    place_name = models.CharField(max_length=300, blank=True)
    place_full_name = models.CharField(max_length=500, blank=True)
    tweet_id = models.CharField(max_length=25, unique=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.username + ': ' + self.body
