# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0005_auto_20150517_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='bounding_box',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tweet',
            name='place_full_name',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tweet',
            name='place_name',
            field=models.CharField(max_length=300, blank=True),
            preserve_default=True,
        ),
    ]
