# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0012_auto_20150920_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='room',
            field=models.OneToOneField(null=True, to='djinn.Room'),
        ),
    ]
