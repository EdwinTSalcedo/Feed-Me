#REGISTRO DE TODOS LOS MODELOS EN LA ADMINISTRACION DE LA APLICACION WEB /ADMIN
from django.contrib import admin
from models import * 
# Register your models here.
class PerfilAdmin(admin.ModelAdmin):
    list_display   = ('user','celular','direccion')
    ordering = ('user',)
    search_fields = ('user',)
    
class RestaurantAdmin(admin.ModelAdmin):
    list_display   = ('id','nombre','direccion','telefono')
    ordering = ('id',)
    search_fields = ('nombre',)

class MesaAdmin(admin.ModelAdmin):
    list_display   = ('id','nombre','restaurant')
    ordering = ('id',)
    search_fields = ('nombre',)

class PlatoAdmin(admin.ModelAdmin):
    list_display   = ('id','nombre','restaurant')
    ordering = ('id',)
    search_fields = ('nombre',)

class BebidaAdmin(admin.ModelAdmin):
    list_display   = ('id','nombre','restaurant')
    ordering = ('id',)
    search_fields = ('nombre',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display   = ('id','nombre','restaurant')
    ordering = ('id',)
    search_fields = ('nombre',)

class PedidoPlatoAdmin(admin.ModelAdmin):
    list_display   = ('id','plato','cantidad','cliente')
    ordering = ('id',)
    search_fields = ('plato',)

class PedidoExtraAdmin(admin.ModelAdmin):
    list_display   = ('id','pedido','cantidad','cliente')
    ordering = ('id',)
    search_fields = ('pedido',)

admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Perfil,PerfilAdmin)
admin.site.register(Mesa,MesaAdmin)
admin.site.register(Plato,PlatoAdmin)
admin.site.register(Bebida,BebidaAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(PedidoPlato,PedidoPlatoAdmin)
admin.site.register(PedidoExtra,PedidoExtraAdmin)
