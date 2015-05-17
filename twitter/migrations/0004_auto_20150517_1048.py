# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_auto_20150517_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='username',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
