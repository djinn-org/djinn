# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0011_client_clientheartbeat_clientupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='alias',
            field=models.CharField(null=True, unique=True, max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='clientheartbeat',
            name='last_heartbeat',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='clientupdate',
            name='failed_updates',
            field=models.IntegerField(default=0),
        ),
    ]
