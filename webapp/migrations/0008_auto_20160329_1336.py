# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20160329_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bebida',
            name='descripcion',
            field=models.TextField(max_length=333, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plato',
            name='descripcion',
            field=models.TextField(max_length=333, blank=True),
            preserve_default=True,
        ),
    ]
