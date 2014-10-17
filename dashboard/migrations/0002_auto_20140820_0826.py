# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='env',
            field=models.ForeignKey(verbose_name='env', to='dashboard.Environment', db_index=False),
        ),
    ]
