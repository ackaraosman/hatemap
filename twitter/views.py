from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('selam naber :)')


def armut(request):
    return HttpResponse('armut')
