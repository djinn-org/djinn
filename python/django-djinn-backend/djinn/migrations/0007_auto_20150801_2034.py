# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0006_auto_20150801_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='minutes',
            field=models.IntegerField(blank=True),
        ),
    ]
