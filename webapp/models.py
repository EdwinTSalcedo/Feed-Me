# coding: utf-8
#REGISTRO DE LOS MODELOS (TABLAS DE BASE DE DATOS)
from __future__ import unicode_literals
from django.contrib.auth.models import *
from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q


class Restaurant(models.Model):
    #OPCIONES PARA EL ESTADO
    opciones = (
        ('activo', 'activo'),
        ('inactivo', 'inactivo'),
        )
    
    nombre = models.CharField(max_length=45,unique=True)
    direccion = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=15, blank=True,verbose_name="Teléfono")
    foto = models.ImageField(upload_to="foto_restaurant/",blank=False,verbose_name = "Logo")
    estado = models.CharField(max_length=200, choices=opciones,blank=True)
    creador = models.ForeignKey(User,default=None,verbose_name = "Creador",blank=True,null=True)
    class Meta:
        #managed = False
        db_table = 'restaurant'
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurantes"

    def __unicode__(self):
        return self.nombre

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45,unique=True)
    restaurant = models.ForeignKey(Restaurant,verbose_name="Restaurant",db_column="restaurant",blank=True)
    
    class Meta:
        #managed = False
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = 'categoria'

    def __unicode__(self):
        return self.nombre 

class Plato(models.Model):
    nombre = models.CharField(max_length=45,unique=True)
    descripcion = models.TextField(max_length=333, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Precio (Bs.)')
    foto = models.ImageField(upload_to="foto_plato/",blank=True,verbose_name = "Fotografia")
    restaurant = models.ForeignKey(Restaurant,verbose_name="Restaurant",db_column="restaurant",blank=True)
    categoria = models.ForeignKey('Categoria', db_column='categoria', verbose_name="Categoria")

    class Meta:
        #managed = False
        db_table = 'plato'
        verbose_name = "Plato"
        verbose_name_plural = "Platos"

    def __unicode__(self):
        return self.nombre

class Bebida(models.Model):
    nombre = models.CharField(max_length=45,unique=True)
    descripcion = models.TextField(max_length=2000, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Precio (Bs.)')
    foto = models.ImageField(upload_to="foto_plato/",blank=False,verbose_name = "Fotografia")
    restaurant = models.ForeignKey(Restaurant,verbose_name="Restaurant",db_column="restaurant",blank=True)
    categoria = models.ForeignKey('Categoria', db_column='categoria', verbose_name="Categoria")

    class Meta:
        #managed = False
        db_table = 'bebida'
        verbose_name = "Bebida"
        verbose_name_plural = "Bebida"

    def __unicode__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(User)
    celular = models.CharField(max_length=15, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    foto = models.ImageField(upload_to="foto_perfil/",blank=True,null=True,verbose_name = "Foto")
    fecha_nacimiento = models.DateField(db_column='fechaNacimiento', blank=True,verbose_name='Fecha de Nacimiento',null=True)
    direccion = models.CharField(max_length=150, blank=True)
    restaurant = models.ManyToManyField(Restaurant,verbose_name="Restaurant",blank=True)
    class Meta: 
        #managed = False
        db_table = 'perfil'
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __unicode__(self):
        return unicode(self.user)

class Mesa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    restaurant = models.ForeignKey(Restaurant,verbose_name="Restaurant",db_column="restaurant")

    class Meta:
        #managed = False
        db_table = 'mesa'
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        unique_together = ('nombre', 'id')

    def __unicode__(self):
        return self.nombre

    def libre(self):
        pedidosplato = PedidoPlato.objects.filter(mesa__id=self.id).exclude(estado="cuenta").count()
        pedidosbebida = PedidoBebida.objects.filter(mesa__id=self.id).exclude(estado="cuenta").count()
        pedidosextra = PedidoBebida.objects.filter(mesa__id=self.id).exclude(estado="cuenta").count()

        if pedidosplato == 0 and pedidosbebida == 0 and pedidosextra == 0:
            return True
        else:
            return False


class PedidoPlato(models.Model):
    opciones = (
        ('pedido', 'pedido'),
        ('entregado', 'entregado'),
        ('cuenta', 'cuenta'),
        )
    id = models.AutoField(primary_key=True)
    mesa = models.ForeignKey(Mesa,verbose_name="Mesa",db_column="mesa")
    cliente = models.ForeignKey(User,default=None,verbose_name = "Cliente")
    plato = models.ForeignKey(Plato,verbose_name="Plato",db_column="plato")
    estado = models.CharField(max_length=200, choices=opciones)
    cantidad = models.IntegerField(default=0,verbose_name="Cantidad",validators=[MinValueValidator(0)])

    class Meta:
        #managed = False
        db_table = 'pedidoplato'
        verbose_name = "Pedido Plato"
        verbose_name_plural = "Pedidos Plato"

    def __unicode__(self):
        return str(self.id)

    def precio(self):
        return cantidad * self.plato.precio

class PedidoBebida(models.Model):
    opciones = (
        ('pedido', 'pedido'),
        ('entregado', 'entregado'),
        ('cuenta', 'cuenta'),
        )
    id = models.AutoField(primary_key=True)
    mesa = models.ForeignKey(Mesa,verbose_name="Mesa",db_column="mesa")
    cliente = models.ForeignKey(User,default=None,verbose_name = "Cliente")
    bebida = models.ForeignKey(Bebida,verbose_name="Bebida",db_column="bebida")
    estado = models.CharField(max_length=200, choices=opciones)
    cantidad = models.IntegerField(default=0,verbose_name="Cantidad",validators=[MinValueValidator(0)])
    class Meta:
        #managed = False
        db_table = 'pedidobebida'
        verbose_name = "Pedido Bebida"
        verbose_name_plural = "Pedidos Bebida"

    def __unicode__(self):
        return str(self.id)

    def precio(self):
        return cantidad * self.bebida.precio

class PedidoExtra(models.Model):
    opciones = (
        ('pedido', 'pedido'),
        ('entregado', 'entregado'),
        )
    id = models.AutoField(primary_key=True)
    mesa = models.ForeignKey(Mesa,verbose_name="Mesa",db_column="mesa")
    cliente = models.ForeignKey(User,default=None,verbose_name = "Cliente")
    pedido = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=200, choices=opciones)
    cantidad = models.IntegerField(default=0,verbose_name="Cantidad",validators=[MinValueValidator(0)])
    class Meta:
        #managed = False
        db_table = 'pedidoextra'
        verbose_name = "Pedido Extra"
        verbose_name_plural = "Pedidos Extra"

    def __unicode__(self):
        return str(self.id)

class RecomendacionRestaurant(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant,verbose_name="Restaurant",db_column="restaurant")
    cliente = models.ForeignKey(User,default=None,verbose_name = "Cliente")
    comentario = models.TextField(max_length=5000, blank=True)

    class Meta:
        #managed = False
        db_table = 'recomendacionrestaurant'
        verbose_name = "Recomendación del Restaurant"
        verbose_name_plural = "Recomendaciones del Restaurant"

    def __unicode__(self):
        return str(self.id)

class RecomendacionCamarero(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant,verbose_name="Restaurant",db_column="restaurant")
    cliente = models.ForeignKey(User,default=None,verbose_name = "Cliente")
    comentario = models.TextField(max_length=5000, blank=True)

    class Meta:
        #managed = False
        db_table = 'recomendacioncamarero'
        verbose_name = "Recomendación del Camarero"
        verbose_name_plural = "Recomendaciones del Camarero"

    def __unicode__(self):
        return str(self.id)

class RecomendacionConsumo(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant,verbose_name="Restaurant",db_column="restaurant")
    cliente = models.ForeignKey(User,default=None,verbose_name = "Cliente")
    comentario = models.TextField(max_length=5000, blank=True)

    class Meta:
        #managed = False
        db_table = 'recomendacionconsumo'
        verbose_name = "Recomendación del Consumo"
        verbose_name_plural = "Recomendaciones del Consumo"

    def __unicode__(self):
        return str(self.id)