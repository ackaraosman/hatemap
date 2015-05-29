# coding: utf-8
from django.contrib.gis import admin
from .models import Tweet

def mark_as_train_hakaret(modeladmin, request, queryset):
    queryset.update(klass='A', train=True)
mark_as_train_hakaret.short_description = 'Mark as Train/Hakaret'


def mark_as_train_irkcilik(modeladmin, request, queryset):
    queryset.update(klass='I', train=True)
mark_as_train_irkcilik.short_description = 'Mark as Train/Irkçılık'


def mark_as_train_homofobi(modeladmin, request, queryset):
    queryset.update(klass='H', train=True)
mark_as_train_homofobi.short_description = 'Mark as Train/Homofobi'


def mark_as_train_notr(modeladmin, request, queryset):
    queryset.update(klass='N', train=True)
mark_as_train_notr.short_description = 'Mark as Train/Notr'


def unmark_classification(modeladmin, request, queryset):
    queryset.update(klass=None)
unmark_classification.short_description = 'Unmark Classification'


class TweetAdmin(admin.OSMGeoAdmin):
    list_display = ['place_name', 'created_at', 'username', 'train', 'klass', 'body']
    list_filter = ['train', 'klass']
    search_fields = ['body']
    actions = [
        mark_as_train_hakaret,
        mark_as_train_irkcilik,
        mark_as_train_homofobi,
        mark_as_train_notr,
        mark_as_not_train,
        unmark_classification,
    ]


admin.site.register(Tweet, TweetAdmin)
