# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0007_auto_20150801_2034'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('building', 'floor', 'name')]),
        ),
    ]
