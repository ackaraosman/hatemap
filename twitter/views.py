from django.shortcuts import render
from django.views.decorators.gzip import gzip_page
from jsonview.decorators import json_view
from .models import Tweet


KLASSES = {
    'irkcilik': 'I',
    'hakaret': 'A',
    'homofobi': 'H',
    'notr': 'N',
}


def home(request):
    return render(request, 'home.html')


@gzip_page
@json_view
def points(request):
    klass_type = request.GET.get('t', 'nb')
    klass = request.GET.get('k', '')
    if klass:
        if klass_type == 'nb':
            tweets = Tweet.objects.filter(klass=KLASSES[klass]).order_by('-id')
        else:
            tweets = Tweet.objects.filter(klass_sci=KLASSES[klass]).order_by('-id')
    else:
        tweets = Tweet.objects.all().order_by('-id')
    points = [[p[0].x, p[0].y] for p in tweets[:5000].values_list('point')]
    return {
        'results': points
    }
