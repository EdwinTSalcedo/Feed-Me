# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20160329_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bebida',
            name='descripcion',
            field=models.TextField(max_length=2000, blank=True),
            preserve_default=True,
        ),
    ]
