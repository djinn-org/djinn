# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import djinn.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('mac', djinn.models.MACAddressField(unique=True, max_length=17)),
                ('alias', models.CharField(blank=True, unique=True, max_length=50, null=True)),
                ('service_url', models.URLField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientHeartbeat',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('last_heartbeat', models.DateTimeField(auto_now=True)),
                ('client', models.OneToOneField(to='djinn.Client')),
            ],
        ),
        migrations.CreateModel(
            name='ClientUpdate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('failed_updates', models.IntegerField(default=0)),
                ('client', models.OneToOneField(to='djinn.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True)),
                ('minutes', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationLog',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('minutes', models.IntegerField()),
                ('log_type', models.CharField(max_length=50, choices=[('create', 'Create'), ('cancel', 'Cancel')])),
                ('log_trigger', models.CharField(max_length=50, choices=[('djinn', 'Djinn'), ('app', 'App'), ('web', 'Web'), ('ext', 'Ext')])),
                ('log_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('floor', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('external_name', models.CharField(unique=True, max_length=20)),
                ('capacity', models.IntegerField()),
                ('building', models.ForeignKey(to='djinn.Building')),
            ],
        ),
        migrations.CreateModel(
            name='RoomEquipment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('equipment', models.ForeignKey(to='djinn.Equipment')),
                ('room', models.ForeignKey(to='djinn.Room')),
            ],
        ),
        migrations.AddField(
            model_name='reservationlog',
            name='room',
            field=models.ForeignKey(to='djinn.Room'),
        ),
        migrations.AddField(
            model_name='reservationlog',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(to='djinn.Room'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='room',
            field=models.OneToOneField(null=True, to='djinn.Room'),
        ),
        migrations.AlterUniqueTogether(
            name='roomequipment',
            unique_together=set([('room', 'equipment')]),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('building', 'floor', 'name')]),
        ),
    ]
