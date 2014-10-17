# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20140820_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='is_enabled',
            field=models.BooleanField(default=True, db_index=True),
            preserve_default=True,
        ),
    ]
