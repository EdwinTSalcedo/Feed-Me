# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_recomendacioncamarero_recomendacionconsumo_recomendacionrestaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesa',
            name='nombre',
            field=models.CharField(max_length=45),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='mesa',
            unique_together=set([('nombre', 'id')]),
        ),
    ]
