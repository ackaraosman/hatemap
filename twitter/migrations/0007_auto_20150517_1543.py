# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0006_auto_20150517_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='bounding_box',
        ),
        migrations.AddField(
            model_name='tweet',
            name='tweet_id',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
