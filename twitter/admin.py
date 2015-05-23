# coding: utf-8
from django.contrib import admin
from .models import Tweet


def mark_as_train(modeladmin, request, queryset):
    queryset.update(train=True)
mark_as_train.short_description = 'Mark as train data'


def mark_as_not_train(modeladmin, request, queryset):
    queryset.update(train=False)
mark_as_not_train.short_description = 'Remove from train data'


def mark_as_abartma(modeladmin, request, queryset):
    queryset.update(klass='A')
mark_as_abartma.short_description = 'Mark as Abartma'


def mark_as_irkcilik(modeladmin, request, queryset):
    queryset.update(klass='I')
mark_as_irkcilik.short_description = 'Mark as Irkçılık'


def mark_as_homofobi(modeladmin, request, queryset):
    queryset.update(klass='H')
mark_as_homofobi.short_description = 'Mark as Homofobi'


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['place_name', 'created_at', 'username', 'train', 'klass', 'body']
    actions = [
        mark_as_train,
        mark_as_not_train,
        mark_as_abartma,
        mark_as_irkcilik,
        mark_as_homofobi,
    ]
