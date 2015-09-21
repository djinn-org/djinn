# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djinn', '0013_auto_20150920_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('minutes', models.IntegerField()),
                ('log_type', models.CharField(choices=[('create', 'Create'), ('cancel', 'Cancel')], max_length=50)),
                ('log_trigger', models.CharField(choices=[('djinn', 'Djinn'), ('app', 'App'), ('web', 'Web'), ('ext', 'Ext')], max_length=50)),
                ('log_time', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(to='djinn.Room')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
