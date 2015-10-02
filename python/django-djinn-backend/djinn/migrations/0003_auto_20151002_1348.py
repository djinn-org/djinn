# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0002_auto_20150929_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='room',
            field=models.OneToOneField(null=True, to='djinn.Room', blank=True),
        ),
    ]
