# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20160318_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='estado',
            field=models.CharField(blank=True, max_length=200, choices=[('activo', 'activo'), ('inactivo', 'inactivo')]),
            preserve_default=True,
        ),
    ]
