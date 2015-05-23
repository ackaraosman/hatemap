# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0009_tweet_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='train',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
