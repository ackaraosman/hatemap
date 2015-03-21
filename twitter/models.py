from django.db import models


class Tweet(models.Model):
    username = models.CharField(max_length=12)
    body = models.CharField(max_length=140)

    def __str__(self):
        return self.username + ': ' + self.body
