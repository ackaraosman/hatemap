from django.shortcuts import render
from jsonview.decorators import json_view
from .models import Tweet


def home(request):
    return render(request, 'home.html')


@json_view
def points(request):
    tweets = Tweet.objects.all()
    points = [[p[0].x, p[0].y] for p in tweets.values_list('point')]
    return {
        'results': points
    }
