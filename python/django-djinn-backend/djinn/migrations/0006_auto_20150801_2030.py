# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0005_auto_20150727_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='minutes',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end',
            field=models.DateTimeField(null=True),
        ),
    ]
