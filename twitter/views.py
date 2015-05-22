from django.shortcuts import render
from django.views.decorators.gzip import gzip_page
from jsonview.decorators import json_view
from .models import Tweet


def home(request):
    return render(request, 'home.html')


@gzip_page
@json_view
def points(request):
    tweets = Tweet.objects.all()
    points = [[p[0].x, p[0].y] for p in tweets.values_list('point')]
    return {
        'results': points
    }
