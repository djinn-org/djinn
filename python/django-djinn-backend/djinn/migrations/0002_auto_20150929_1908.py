# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djinn', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('mac',)},
        ),
        migrations.AlterModelOptions(
            name='equipment',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ('room', 'start', 'minutes')},
        ),
        migrations.AlterModelOptions(
            name='reservationlog',
            options={'ordering': ('log_time',)},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ('external_name',)},
        ),
        migrations.AlterField(
            model_name='client',
            name='alias',
            field=models.CharField(null=True, blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='client',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='client',
            name='service_url',
            field=models.URLField(),
        ),
    ]
