# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bebida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=45)),
                ('descripcion', models.TextField(max_length=5000, blank=True)),
                ('precio', models.DecimalField(verbose_name='Precio (Bs.)', max_digits=10, decimal_places=2)),
                ('foto', models.ImageField(upload_to='foto_plato/', verbose_name='Fotografia')),
            ],
            options={
                'db_table': 'bebida',
                'verbose_name': 'Bebida',
                'verbose_name_plural': 'Bebida',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'categoria',
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=45)),
            ],
            options={
                'db_table': 'mesa',
                'verbose_name': 'Mesa',
                'verbose_name_plural': 'Mesas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PedidoBebida',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('estado', models.CharField(max_length=200, choices=[('pedido', 'pedido'), ('entregado', 'entregado'), ('cuenta', 'cuenta')])),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad', validators=[django.core.validators.MinValueValidator(0)])),
                ('bebida', models.ForeignKey(db_column='bebida', verbose_name='Bebida', to='webapp.Bebida')),
                ('cliente', models.ForeignKey(default=None, verbose_name='Cliente', to=settings.AUTH_USER_MODEL)),
                ('mesa', models.ForeignKey(db_column='mesa', verbose_name='Mesa', to='webapp.Mesa')),
            ],
            options={
                'db_table': 'pedidobebida',
                'verbose_name': 'Pedido Bebida',
                'verbose_name_plural': 'Pedidos Bebida',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PedidoExtra',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('pedido', models.CharField(max_length=15, blank=True)),
                ('estado', models.CharField(max_length=200, choices=[('pedido', 'pedido'), ('entregado', 'entregado')])),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad', validators=[django.core.validators.MinValueValidator(0)])),
                ('cliente', models.ForeignKey(default=None, verbose_name='Cliente', to=settings.AUTH_USER_MODEL)),
                ('mesa', models.ForeignKey(db_column='mesa', verbose_name='Mesa', to='webapp.Mesa')),
            ],
            options={
                'db_table': 'pedidoextra',
                'verbose_name': 'Pedido Extra',
                'verbose_name_plural': 'Pedidos Extra',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PedidoPlato',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('estado', models.CharField(max_length=200, choices=[('pedido', 'pedido'), ('entregado', 'entregado'), ('cuenta', 'cuenta')])),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad', validators=[django.core.validators.MinValueValidator(0)])),
                ('cliente', models.ForeignKey(default=None, verbose_name='Cliente', to=settings.AUTH_USER_MODEL)),
                ('mesa', models.ForeignKey(db_column='mesa', verbose_name='Mesa', to='webapp.Mesa')),
            ],
            options={
                'db_table': 'pedidoplato',
                'verbose_name': 'Pedido Plato',
                'verbose_name_plural': 'Pedidos Plato',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('celular', models.CharField(max_length=15, blank=True)),
                ('telefono', models.CharField(max_length=15, blank=True)),
                ('foto', models.ImageField(upload_to='foto_perfil/', null=True, verbose_name='Foto', blank=True)),
                ('fecha_nacimiento', models.DateField(null=True, verbose_name='Fecha de Nacimiento', db_column='fechaNacimiento', blank=True)),
                ('direccion', models.CharField(max_length=150, blank=True)),
            ],
            options={
                'db_table': 'perfil',
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=45)),
                ('descripcion', models.TextField(max_length=5000, blank=True)),
                ('precio', models.DecimalField(verbose_name='Precio (Bs.)', max_digits=10, decimal_places=2)),
                ('foto', models.ImageField(upload_to='foto_plato/', verbose_name='Fotografia', blank=True)),
                ('categoria', models.ForeignKey(db_column='categoria', verbose_name='Categoria', to='webapp.Categoria')),
            ],
            options={
                'db_table': 'plato',
                'verbose_name': 'Plato',
                'verbose_name_plural': 'Platos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=45)),
                ('direccion', models.CharField(max_length=150, blank=True)),
                ('telefono', models.CharField(max_length=15, verbose_name='Tel\xe9fono', blank=True)),
                ('foto', models.ImageField(upload_to='foto_restaurant/', verbose_name='Logo')),
                ('estado', models.CharField(max_length=200, choices=[('activo', 'activo'), ('inactivo', 'inactivo')])),
                ('creador', models.ForeignKey(default=None, verbose_name='Creador', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'restaurant',
                'verbose_name': 'Restaurant',
                'verbose_name_plural': 'Restaurantes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='plato',
            name='restaurant',
            field=models.ForeignKey(db_column='restaurant', verbose_name='Restaurant', blank=True, to='webapp.Restaurant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='restaurant',
            field=models.ManyToManyField(to='webapp.Restaurant', verbose_name='Restaurant', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pedidoplato',
            name='plato',
            field=models.ForeignKey(db_column='plato', verbose_name='Plato', to='webapp.Plato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mesa',
            name='restaurant',
            field=models.ForeignKey(db_column='restaurant', verbose_name='Restaurant', to='webapp.Restaurant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoria',
            name='restaurant',
            field=models.ForeignKey(db_column='restaurant', verbose_name='Restaurant', blank=True, to='webapp.Restaurant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bebida',
            name='categoria',
            field=models.ForeignKey(db_column='categoria', verbose_name='Categoria', to='webapp.Categoria'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bebida',
            name='restaurant',
            field=models.ForeignKey(db_column='restaurant', verbose_name='Restaurant', blank=True, to='webapp.Restaurant'),
            preserve_default=True,
        ),
    ]
