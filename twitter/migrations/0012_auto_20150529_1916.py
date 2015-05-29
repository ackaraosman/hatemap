# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0011_tweet_klass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='klass',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[('A', 'Hakaret'), ('H', 'Homofobi'), ('I', 'Irk\xe7\u0131l\u0131k'), ('N', 'N\xf6tr')]),
            preserve_default=True,
        ),
    ]
