from django.shortcuts import render
from django.views.decorators.gzip import gzip_page
from django.db.models import Q
from jsonview.decorators import json_view
from unidecode import unidecode
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
    klass_type = request.GET.get('t', '')
    klass = request.GET.get('k', '')
    q = request.GET.get('q')

    tweets = Tweet.objects.all()
    if klass:
        if klass_type == 'svm':
            tweets = tweets.filter(klass_svm=KLASSES[klass])
        elif klass_type == 'nb':
            tweets = tweets.filter(klass=KLASSES[klass])
        else:
            tweets = tweets.filter(klass=KLASSES[klass], klass_svm=KLASSES[klass])
    if q:
        tweets = tweets.filter(Q(body__icontains=q) | Q(body__icontains=unidecode(q)))
    tweets = tweets.order_by('-id')

    points = [[p[0].x, p[0].y] for p in tweets[:5000].values_list('point')]
    return {
        'results': points
    }
