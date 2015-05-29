# coding: utf-8
from __future__ import unicode_literals, print_function
from django.contrib.gis.db import models


class Tweet(models.Model):
    CLASSES = [
        ('A', 'Hakaret'),
        ('H', 'Homofobi'),
        ('I', 'Irkçılık'),
        ('N', 'Nötr'),
    ]
    username = models.CharField(max_length=20)
    body = models.TextField()
    point = models.PointField(null=True, blank=True)
    place_name = models.CharField(max_length=300, blank=True)
    place_full_name = models.CharField(max_length=500, blank=True)
    tweet_id = models.CharField(max_length=25, unique=True)
    objects = models.GeoManager()
    created_at = models.DateTimeField(null=True, blank=True)
    train = models.BooleanField(default=False)
    klass = models.CharField(max_length=2, choices=CLASSES, null=True, blank=True)


    def __unicode__(self):
        return self.username + ': ' + self.body
