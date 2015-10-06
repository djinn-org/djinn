# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0004_client_enabled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservationlog',
            options={'ordering': ('-log_time',)},
        ),
    ]
