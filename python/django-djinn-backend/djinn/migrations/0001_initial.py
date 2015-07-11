# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('building', models.CharField(max_length=20)),
                ('floor', models.IntegerField()),
                ('number', models.IntegerField()),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomEquipment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('equipment', models.ForeignKey(to='djinn.Equipment')),
                ('room', models.ForeignKey(to='djinn.Room')),
            ],
        ),
    ]
