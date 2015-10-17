# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0005_auto_20151006_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationlog',
            name='reservation_pk',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
