# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0013_tweet_klass_sci'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='klass_sci',
            new_name='klass_svm',
        ),
    ]
