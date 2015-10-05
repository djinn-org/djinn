# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0003_auto_20151002_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
