# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20160327_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoextra',
            name='pedido',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
