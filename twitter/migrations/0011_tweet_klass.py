# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0010_tweet_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='klass',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'A', b'Abartma'), (b'H', b'Homofobi'), (b'I', b'Irk\xc3\xa7\xc4\xb1l\xc4\xb1k')]),
            preserve_default=True,
        ),
    ]
