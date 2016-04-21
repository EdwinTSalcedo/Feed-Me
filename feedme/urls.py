# coding: utf-8
# ARCHIVO PARA LA CONFIGURACION DE LAS URL
from django.conf.urls import patterns, include, url
from webapp.views import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
import settings

#CONFIGURACION DE URLS DE LA APLICACION
urlpatterns = patterns('webapp.views',
    # Examples:
    # url(r'^$', 'feedme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'control_ingreso', name='control_ingreso'),
    url(r'^login/$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^home/$', "home", name="home"),
    url(r'^error/$', "error", name="error"),
    url(r'^fail/$', "fail", name="fail"),
    url(r'^logout/$', logout, {'template_name': 'error.html', }, name="logout"),
    url(r'^signup/$','nuevo_usuario'),
    url(r'^perfil/$', "perfil", name="perfil"),
    url(r'^actualizar/usuario/$', "actualizar_usuario", name="actualizar_usuario"),
    url(r'^actualizar/password/$', "actualizar_password", name="actualizar_password"),
    url(r'^actualizar/mesas/(?P<operacion>.*)/$', "actualizar_mesas", name="actualizar_mesas"),
    url(r'^actualizar/pedido/(?P<tipo>.*)/(?P<id_pedido>.*)/$', "actualizar_pedido", name="actualizar_pedido"),


    url(r'^personal/$', "personal"),
    url(r'^bebidas/$', "bebidas"),
    url(r'^platos/$', "platos"),
    url(r'^mesas/$', "mesas"),
    url(r'^restaurantes/$', "restaurantes"),
    url(r'^categorias/$', "categorias"),
    url(r'^cocina/$', "cocina"),
    url(r'^bar/$', "bar"),

    url(r'^agregar/empleado/$', "nuevo_empleado"),
    url(r'^agregar/bebida/$', "nuevo_bebida"),
    url(r'^agregar/plato/$', "nuevo_plato"),
    url(r'^agregar/restaurant/$', "nuevo_restaurant"),
    url(r'^agregar/categoria/$', "nuevo_categoria"),

    url(r'^detalle/mesa/(?P<id_mesa>.*)/$', "detalle_mesa"),

    url(r'^editar/empleado/(?P<id_empleado>.*)/$', "editar_empleado"),
    url(r'^editar/bebida/(?P<id_bebida>.*)/$', "editar_bebida"),
    url(r'^editar/plato/(?P<id_plato>.*)/$', "editar_plato"),
    url(r'^editar/restaurant/(?P<id_restaurant>.*)/$', "editar_restaurant"),
    url(r'^editar/categoria/(?P<id_categoria>.*)/$', "editar_categoria"),

    url(r'^cambiar/restaurant/(?P<id_restaurant>.*)/$', "cambiar_restaurant"),
    
    url(r'^eliminar/empleado/(?P<id_empleado>.*)/$', "eliminar_empleado"),  
    url(r'^eliminar/bebida/(?P<id_bebida>.*)/$', "eliminar_bebida"),  
    url(r'^eliminar/plato/(?P<id_plato>.*)/$', "eliminar_plato"),   
    url(r'^eliminar/restaurant/(?P<id_restaurant>.*)/$', "eliminar_restaurant"),   
    url(r'^eliminar/categoria/(?P<id_categoria>.*)/$', "eliminar_categoria"),   
)
#CONFIGURACION DE URLS DE LA APLICACION MOVIL
urlpatterns += patterns('mobileapp.views',
    url(r'^cliente/(?P<id_mesa>.*)/$', 'control_ingreso_cliente',name='control_ingreso_cliente'),
    url(r'^login/cliente/(?P<id_mesa>.*)/$', "login_cliente",name="login_cliente"),
    url(r'^home/cliente/(?P<id_mesa>.*)/$', "home",name="home_cliente"),
    url(r'^error/cliente/$', "error_cliente", name="error_cliente"),
    url(r'^logout/cliente/$', "logout_cliente", name="logout_cliente"),
    url(r'^signup/cliente/(?P<id_mesa>.*)/$','nuevo_usuario_cliente'),
    url(r'^menu/cliente/(?P<id_mesa>.*)/$', "menu",name="menu_cliente"),
    url(r'^pedido/(?P<tipo>.*)/(?P<id_mesa>.*)/(?P<id_elemento>.*)/$', "pedido",name="pedido_cliente"),
    url(r'^cancelar/(?P<tipo>.*)/(?P<id_pedido>.*)/$', "cancelar",name="cancelarpedido_cliente"),
    url(r'^cuentatotal/cliente/(?P<id_mesa>.*)/$', "cuentatotal",name="cuentatotal"),
    url(r'^cuentapropia/cliente/(?P<id_mesa>.*)/$', "cuentapropia",name="cuentapropia"),
    url(r'^pedidoextra/cliente/(?P<id_mesa>.*)/$', "pedidoextra",name="pedidoextra"),
    url(r'^pedircuenta/cliente/(?P<id_mesa>.*)/$', "pedircuenta",name="pedircuenta"),
    url(r'^recomendaciones/cliente/(?P<id_mesa>.*)/$', "recomendaciones",name="recomendaciones"),
    #url(r'^signup/cliente/$','nuevo_usuario'),
)

#URL RECUPERACION CONTRASEÑA
urlpatterns += patterns('',
     url(r'^reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/reset/done'},
        name="password_reset"),
    (r'^reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/login'}),
    (r'^done/$', 
        'django.contrib.auth.views.password_reset_complete'),
)

#CARGA DE MEDIA
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),)