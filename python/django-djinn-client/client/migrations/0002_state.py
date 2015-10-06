# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('state', models.CharField(choices=[('none', 'None'), ('empty', 'Empty'), ('presence', 'Presence')], default='none', max_length=50)),
            ],
        ),
    ]
