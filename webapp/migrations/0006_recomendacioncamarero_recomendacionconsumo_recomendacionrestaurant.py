# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0005_auto_20160329_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecomendacionCamarero',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('comentario', models.TextField(max_length=5000, blank=True)),
                ('cliente', models.ForeignKey(default=None, verbose_name='Cliente', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(db_column='restaurant', verbose_name='Restaurant', to='webapp.Restaurant')),
            ],
            options={
                'db_table': 'recomendacioncamarero',
                'verbose_name': 'Recomendaci\xf3n del Camarero',
                'verbose_name_plural': 'Recomendaciones del Camarero',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecomendacionConsumo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('comentario', models.TextField(max_length=5000, blank=True)),
                ('cliente', models.ForeignKey(default=None, verbose_name='Cliente', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(db_column='restaurant', verbose_name='Restaurant', to='webapp.Restaurant')),
            ],
            options={
                'db_table': 'recomendacionconsumo',
                'verbose_name': 'Recomendaci\xf3n del Consumo',
                'verbose_name_plural': 'Recomendaciones del Consumo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecomendacionRestaurant',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('comentario', models.TextField(max_length=5000, blank=True)),
                ('cliente', models.ForeignKey(default=None, verbose_name='Cliente', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(db_column='restaurant', verbose_name='Restaurant', to='webapp.Restaurant')),
            ],
            options={
                'db_table': 'recomendacionrestaurant',
                'verbose_name': 'Recomendaci\xf3n del Restaurant',
                'verbose_name_plural': 'Recomendaciones del Restaurant',
            },
            bases=(models.Model,),
        ),
    ]
