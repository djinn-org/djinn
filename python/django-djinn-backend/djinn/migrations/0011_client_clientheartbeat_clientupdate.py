# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djinn.models


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0010_auto_20150906_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('mac', djinn.models.MACAddressField(max_length=17, unique=True)),
                ('alias', models.TextField(null=True, unique=True)),
                ('service_url', models.URLField(unique=True)),
                ('room', models.ForeignKey(unique=True, null=True, to='djinn.Room')),
            ],
        ),
        migrations.CreateModel(
            name='ClientHeartbeat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('last_heartbeat', models.DateTimeField()),
                ('client', models.OneToOneField(to='djinn.Client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('failed_updates', models.IntegerField()),
                ('client', models.OneToOneField(to='djinn.Client')),
            ],
        ),
    ]
