# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20141017_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environment',
            name='id',
        ),
        migrations.RemoveField(
            model_name='host',
            name='id',
        ),
        migrations.RemoveField(
            model_name='role',
            name='id',
        ),
        migrations.AlterField(
            model_name='environment',
            name='name',
            field=models.CharField(max_length=20, serialize=False, verbose_name='name', primary_key=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='env',
            field=models.ForeignKey(related_name='hosts', verbose_name='env', to='dashboard.Environment', db_index=False),
        ),
        migrations.AlterField(
            model_name='host',
            name='name',
            field=models.CharField(max_length=255, serialize=False, verbose_name='name', primary_key=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='roles',
            field=models.ManyToManyField(related_name='hosts', to=b'dashboard.Role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=20, serialize=False, verbose_name='name', primary_key=True, db_index=True),
        ),
    ]
