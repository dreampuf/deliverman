# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_host_is_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='environment',
            name='is_enabled',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='role',
            name='is_enabled',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='env',
            field=models.ForeignKey(related_name='host_hosts', verbose_name='env', to='dashboard.Environment', db_index=False),
        ),
    ]
