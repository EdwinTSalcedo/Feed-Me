# coding: utf-8
#ARCHIVO PARA DEFINIR LAS VISTAS Y FUNCIONES DE LA APLICACION WEB
from django.shortcuts import render_to_response, get_object_or_404,redirect
from webapp.models import *
from django.template import RequestContext,loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from webapp.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from datetime import datetime, timedelta,date,time
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.utils import formats
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

#CONTROL DE INGRESO PARA USUARIOS CON UNA SESION NUEVA
def control_ingreso(request):
    if request.user.is_authenticated():
        verificar_perfil(request)
        return HttpResponseRedirect('/home') 
    else:
        return HttpResponseRedirect('/login')

#VISTA PRINCIPAL DE LA APLICACION
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def home(request):
    mirestaurant = verificar_perfil(request)
    # areas_radiologia, area_preferencia, establecimiento_preferencia = verificar_preferencias(request)
    mesas = Mesa.objects.filter(restaurant=mirestaurant).count()
    platos = Plato.objects.filter(restaurant=mirestaurant).count()
    empleados = User.objects.filter(perfil__restaurant=mirestaurant).count()
    bebidas = Bebida.objects.filter(restaurant=mirestaurant).count()

    # pacientes = Expediente.objects.filter(establecimiento=establecimiento_preferencia).count()
    # citas = Cita.objects.filter(solicitud__expediente__establecimiento=establecimiento_preferencia,estado="Programado").count()
    # areas = AreaRadiologia.objects.all().count()

    ctx = {'restaurant':mirestaurant,'mesas':mesas,'platos':platos,'empleados':empleados,'bebidas':bebidas}
    return render_to_response('webapp/home.html', ctx, context_instance=RequestContext(request))

#VISTA DE ERROR DE LA APLICACION
def error(request):
    redirect_to = None
    try:
        redirect_to = request.REQUEST.get('next', '')
    except request.REQUEST.DoesNotExist:
        redirect_to = None

    ctx = {'redirect_to':redirect_to}

    return render_to_response('error.html',ctx,context_instance=RequestContext(request))

#VISTA DE ERROR DE LA APLICACION
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def fail(request):
    # areas_radiologia, area_preferencia, establecimiento_preferencia = verificar_preferencias(request)

    ctx = {
    # 'areas_radiologia':areas_radiologia,'area_preferencia':area_preferencia
    }

    return render_to_response('webapp/fail.html',ctx,context_instance=RequestContext(request))

#VISTA DEL PEFIL DE CADA USUARIO
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def perfil(request):
    mirestaurant = verificar_perfil(request)
    info_enviado = None
    try:
        info_enviado = request.REQUEST.get('info_enviado', '')
    except request.REQUEST.DoesNotExist:
        info_enviado = None

    pass_form = PasswordChangeForm(user=request.user)
    user_form = MiUserForm(instance=request.user)
    perfil_form = PerfilForm(instance=request.user.perfil)

    ctx = {'info_enviado':info_enviado,'pass_form':pass_form,'user_form':user_form,'perfil_form':perfil_form,"restaurant":mirestaurant}
    return render_to_response('webapp/perfil.html', ctx, context_instance=RequestContext(request))

#VISTA DE ERROR DE LA APLICACION
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def actualizar_usuario(request):
    if request.method == 'POST':
        user_form = MiUserForm(request.POST, request.FILES,instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES ,instance=request.user.perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            return HttpResponseRedirect("/perfil?info_enviado=%d"%1)
        else:
            info_enviado = "Verificá los datos ingresados."
            return HttpResponseRedirect("/perfil?info_enviado=%d"%2)       

#FUNCION PARA ACTUALIZAR EL PASSWORD DE UN USUARIO
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def actualizar_password(request):
    info_enviado = None

    if request.method=='POST':
        formulario =  PasswordChangeForm(user=request.user,data=request.POST)
        if formulario.is_valid():
            info_enviado = "Tu nueva contraseña ha sido registrada." 
            formulario.save()
            return HttpResponseRedirect("/perfil?info_enviado=%d"%3)    
        else:
            info_enviado = "Verificá los datos ingresados."
            return HttpResponseRedirect("/perfil?info_enviado=%d"%4)

#VISTA DEL LISTADO DE PERSONAL
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def personal(request):
    mirestaurant = verificar_perfil(request)
    users = User.objects.filter(perfil__restaurant=mirestaurant).exclude(id=request.user.id)
    ctx = {'users':users,'restaurant':mirestaurant}
    return render_to_response('webapp/personal.html',ctx,context_instance=RequestContext(request))

#VISTA DEL LISTADO DE BEBIDAS
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def bebidas(request):
    mirestaurant = verificar_perfil(request)
    bebidas = Bebida.objects.filter(restaurant=mirestaurant)
    ctx = {'bebidas':bebidas,'restaurant':mirestaurant}
    return render_to_response('webapp/bebidas.html',ctx,context_instance=RequestContext(request))

#VISTA DEL LISTADO DE PLATOS
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def platos(request):
    mirestaurant = verificar_perfil(request)
    platos = Plato.objects.filter(restaurant=mirestaurant)
    ctx = {'platos':platos,'restaurant':mirestaurant}
    return render_to_response('webapp/platos.html',ctx,context_instance=RequestContext(request))

#VISTA DEL LISTADO DE MESAS
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def mesas(request):
    mirestaurant = verificar_perfil(request)
    mesas = Mesa.objects.filter(restaurant=mirestaurant)

    ctx = {'mesas':mesas,'restaurant':mirestaurant}
    return render_to_response('webapp/mesas.html',ctx,context_instance=RequestContext(request))

#VISTA DEL LISTADO DE RESTAURANTES
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def restaurantes(request):
    mirestaurant = verificar_perfil(request)
    restaurantes = Restaurant.objects.filter(creador=request.user)
    ctx = {'restaurantes':restaurantes,'restaurant':mirestaurant}
    return render_to_response('webapp/restaurantes.html',ctx,context_instance=RequestContext(request))

#VISTA DEL LISTADO DE CATEGORIAS
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def categorias(request):
    mirestaurant = verificar_perfil(request)
    categorias = Categoria.objects.filter(restaurant=mirestaurant)
    ctx = {'categorias':categorias,'restaurant':mirestaurant}
    return render_to_response('webapp/categorias.html',ctx,context_instance=RequestContext(request))

#VISTA DEL LISTADO DE COCINA
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Cocina","Bar"]).count() > 0, login_url='/error/')
def cocina(request):
    mirestaurant = verificar_perfil(request)
    pedidos = PedidoPlato.objects.filter(mesa__restaurant=mirestaurant).exclude(estado="cuenta").order_by('-estado')
    ctx = {'pedidos':pedidos,'restaurant':mirestaurant}
    return render_to_response('webapp/cocina.html',ctx,context_instance=RequestContext(request))

#VISTA DEL LISTADO DE BAR
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Cocina","Bar"]).count() > 0, login_url='/error/')
def bar(request):
    mirestaurant = verificar_perfil(request)
    pedidos = PedidoBebida.objects.filter(mesa__restaurant=mirestaurant).exclude(estado="cuenta").order_by('-estado')
    ctx = {'pedidos':pedidos,'restaurant':mirestaurant}
    return render_to_response('webapp/bar.html',ctx,context_instance=RequestContext(request))

#DETALLE DE UNA MESA Y SUS PEDIDOS
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Administradores","Camareros","Runners","Cocina","Bar"]).count() > 0, login_url='/error/')
def detalle_mesa(request,id_mesa):
    mirestaurant = verificar_perfil(request)
    mesa = Mesa.objects.get(id=id_mesa)
    pedidosplato = PedidoPlato.objects.filter(mesa=mesa,estado="pedido")
    pedidosbebida = PedidoBebida.objects.filter(mesa=mesa,estado="pedido")
    pedidosextra = PedidoExtra.objects.filter(mesa=mesa,estado="pedido")

    pedidosplatocompletado = PedidoPlato.objects.filter(mesa=mesa,estado="entregado")
    pedidosbebidacompletado = PedidoBebida.objects.filter(mesa=mesa,estado="entregado")
    pedidosextracompletado = PedidoExtra.objects.filter(mesa=mesa,estado="entregado")

    ctx = {'mesa':mesa,'pedidosplato':pedidosplato,'pedidosbebida':pedidosbebida,'pedidosextra':pedidosextra,'pedidosplatocompletado':pedidosplatocompletado,'pedidosbebidacompletado':pedidosbebidacompletado,'pedidosextracompletado':pedidosextracompletado,'restaurant':mirestaurant}
    return render_to_response('webapp/detalle_mesa.html',ctx,context_instance=RequestContext(request))
##############################################################################################################

#VISTA PARA LA CREACION DE UN USUARIO
def nuevo_usuario(request):
    if request.method=='POST':
        formulario_user = UserCreationForm(request.POST)
        formulario_restaurant = RestaurantForm(request.POST, request.FILES)

        if formulario_user.is_valid() and formulario_restaurant.is_valid():
            user = formulario_user.save()

            mirestaurant = formulario_restaurant.save()
            mirestaurant.creador = user
            mirestaurant.estado = "activo"
            mirestaurant.save()
            perfil = Perfil(user=user,fecha_nacimiento=date(1980, 1, 1,), foto="foto_perfil/defaultprofile.png")
            perfil.save()
            perfil.restaurant.add(mirestaurant)
            administradores = Group.objects.get(name='Administradores') 
            administradores.user_set.add(user)

            return HttpResponseRedirect('/')
        else:
            formulario_restaurant.fields['estado'].widget = forms.HiddenInput()
            formulario_restaurant.fields['creador'].widget = forms.HiddenInput()
    else:
        formulario_user = UserCreationForm()
        formulario_restaurant = RestaurantForm(initial={'estado':'activo'})
        formulario_restaurant.fields['estado'].widget = forms.HiddenInput()
        formulario_restaurant.fields['creador'].widget = forms.HiddenInput()
    return render_to_response('nuevousuario.html',{'formulario_user':formulario_user,'formulario_restaurant':formulario_restaurant},context_instance=RequestContext(request))

#VISTA PARA LA CREACION DE UN EMPLEADO
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def nuevo_empleado(request):
    mirestaurant = verificar_perfil(request)
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = UserForm(request.POST) 
        if form.is_valid():
            registro = form.save()
            perfil = Perfil(user=registro,fecha_nacimiento=date(1980, 1, 1,), foto="foto_perfil/defaultprofile.png")
            perfil.save()
            perfil.restaurant.add(mirestaurant)

            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['groups'].queryset = Group.objects.exclude(name='Administradores')
            # form.fields['responsable'].widget = forms.HiddenInput()
            # form.fields['estado'].widget = forms.HiddenInput()
    else:
        form = UserForm(initial={'hidden_redirect':redirect_to,})
        form.fields['groups'].queryset = Group.objects.exclude(name__in=['Administradores','Clientes'])

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}
    return render_to_response('webapp/nuevo_empleado.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA CREACION DE UNA BEBIDA
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def nuevo_bebida(request):
    mirestaurant = verificar_perfil(request)
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = BebidaForm(request.POST, request.FILES) 
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['restaurant'].widget = forms.HiddenInput()
            # form.fields['responsable'].widget = forms.HiddenInput()
            # form.fields['estado'].widget = forms.HiddenInput()
    else:
        form = BebidaForm(initial={'hidden_redirect':redirect_to,'restaurant':mirestaurant})
        form.fields['restaurant'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}
    return render_to_response('webapp/nuevo_bebida.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA CREACION DE UN PLATO
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def nuevo_plato(request):
    mirestaurant = verificar_perfil(request)
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES) 
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['restaurant'].widget = forms.HiddenInput()
            # form.fields['responsable'].widget = forms.HiddenInput()
            # form.fields['estado'].widget = forms.HiddenInput()
    else:
        form = PlatoForm(initial={'hidden_redirect':redirect_to,'restaurant':mirestaurant})
        form.fields['restaurant'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}
    return render_to_response('webapp/nuevo_plato.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA CREACION DE UN RESTAURANT
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def nuevo_restaurant(request):
    mirestaurant = verificar_perfil(request)
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES) 
        if form.is_valid():
            registro = form.save()

            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['creador'].widget = forms.HiddenInput()
            form.fields['estado'].widget = forms.HiddenInput()
            # form.fields['responsable'].widget = forms.HiddenInput()
            # form.fields['estado'].widget = forms.HiddenInput()
    else:
        form = RestaurantForm(initial={'hidden_redirect':redirect_to,'creador':request.user})
        form.fields['creador'].widget = forms.HiddenInput()
        form.fields['estado'].widget = forms.HiddenInput()
        #form.fields['restaurant'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}
    return render_to_response('webapp/nuevo_restaurant.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA CREACION DE UNA CATEGORIA
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def nuevo_categoria(request):
    mirestaurant = verificar_perfil(request)
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES) 
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['restaurant'].widget = forms.HiddenInput()
            # form.fields['responsable'].widget = forms.HiddenInput()
            # form.fields['estado'].widget = forms.HiddenInput()
    else:
        form = CategoriaForm(initial={'hidden_redirect':redirect_to,'restaurant':mirestaurant})
        form.fields['restaurant'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}
    return render_to_response('webapp/nuevo_categoria.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA EDICION DE UN EMPLEADO
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def editar_empleado(request,id_empleado):

    empleado = User.objects.get(id=id_empleado)

    redirect_to = request.REQUEST.get('next', '')

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=empleado)
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['groups'].queryset = Group.objects.exclude(name='Administradores')
            form.fields['password'].widget = forms.HiddenInput()
    else:
        form = UserForm(instance=empleado)
        form.fields['groups'].queryset = Group.objects.exclude(name__in=['Administradores','Clientes'])
        form.fields['password'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to}

    return render_to_response('webapp/editar_empleado.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA EDICION DE UNA BEBIDA
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def editar_bebida(request,id_bebida):
    mirestaurant = verificar_perfil(request)
    bebida = Bebida.objects.get(id=id_bebida)

    redirect_to = request.REQUEST.get('next', '')

    if request.method == 'POST':
        form = BebidaForm(request.POST, request.FILES,instance=bebida)
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['restaurant'].widget = forms.HiddenInput()
    else:
        form = BebidaForm(instance=bebida)
        form.fields['restaurant'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}

    return render_to_response('webapp/editar_bebida.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA EDICION DE UN PLATO
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def editar_plato(request,id_plato):
    mirestaurant = verificar_perfil(request)
    plato = Plato.objects.get(id=id_plato)

    redirect_to = request.REQUEST.get('next', '')

    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES,instance=plato)
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['restaurant'].widget = forms.HiddenInput()
    else:
        form = PlatoForm(instance=plato)
        form.fields['restaurant'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}

    return render_to_response('webapp/editar_plato.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA EDICION DE UN RESTAURANT
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def editar_restaurant(request,id_restaurant):
    mirestaurant = verificar_perfil(request)
    restaurant = Restaurant.objects.get(id=id_restaurant)

    redirect_to = request.REQUEST.get('next', '')

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES,instance=restaurant)
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['creador'].widget = forms.HiddenInput()
            form.fields['estado'].widget = forms.HiddenInput()
    else:
        form = RestaurantForm(instance=restaurant)
        form.fields['creador'].widget = forms.HiddenInput()
        form.fields['estado'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}

    return render_to_response('webapp/editar_plato.html',ctx,context_instance=RequestContext(request))

#VISTA PARA LA EDICION DE UNA CATEGORIA
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def editar_categoria(request,id_categoria):
    mirestaurant = verificar_perfil(request)
    categoria = Categoria.objects.get(id=id_categoria)

    redirect_to = request.REQUEST.get('next', '')

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES,instance=categoria)
        if form.is_valid():
            registro = form.save()
            if not redirect_to:
                redirect_to = form.cleaned_data['hidden_redirect']
            return HttpResponseRedirect(redirect_to)
        else:
            if not redirect_to:
                redirect_to = form.data['hidden_redirect']
            form.fields['restaurant'].widget = forms.HiddenInput()
    else:
        form = CategoriaForm(instance=categoria)
        form.fields['restaurant'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'restaurant':mirestaurant}

    return render_to_response('webapp/editar_categoria.html',ctx,context_instance=RequestContext(request))

#FUNCION PARA ELIMINAR UN EMPLEADO
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def eliminar_empleado(request,id_empleado):
    empleado = User.objects.get(id=id_empleado)
    empleado.delete()
    redirect_to = request.REQUEST.get('next', '')
    return HttpResponseRedirect(redirect_to)

#FUNCION PARA ELIMINAR UNA BEBIDA
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def eliminar_bebida(request,id_bebida):
    bebida = Bebida.objects.get(id=id_bebida)
    bebida.delete()
    redirect_to = request.REQUEST.get('next', '')
    return HttpResponseRedirect(redirect_to)

#FUNCION PARA ELIMINAR UN PLATO
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def eliminar_plato(request,id_plato):
    plato = Plato.objects.get(id=id_plato)
    plato.delete()
    redirect_to = request.REQUEST.get('next', '')
    return HttpResponseRedirect(redirect_to)

#FUNCION PARA ELIMINAR UN RESTAURANT
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def eliminar_restaurant(request,id_restaurant):
    restaurant = Restaurant.objects.get(id=id_restaurant)
    restaurant.delete()
    redirect_to = request.REQUEST.get('next', '')
    return HttpResponseRedirect(redirect_to)

#FUNCION PARA ELIMINAR UNA CATEGORIA
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def eliminar_categoria(request,id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    categoria.delete()
    redirect_to = request.REQUEST.get('next', '')
    return HttpResponseRedirect(redirect_to)

#FUNCION PARA LA EXISTENCIA DE UN PERFIL Y DEVOLVER UN OBJETO RESTAURANT, ESTO SIRVE PARA OBTENER EL RESTAURANT ASOCIADO A UN USUARIO
def verificar_perfil(request):
    if Perfil.objects.filter(user=request.user).exists():
        if request.user.groups.filter(name="Administradores").count() > 0:
            mirestaurant = Restaurant.objects.get(estado="activo",creador=request.user)
        else:
            mirestaurant = Restaurant.objects.filter(perfil__user=request.user)[0]
    else:
        mirestaurant = Restaurant.objects.get_or_create(nombre="Default",estado="activo",creador=request.user) 
        perfil = Perfil.objects.get_or_create(user=request.user,fecha_nacimiento=date(1980, 1, 1,), foto="foto_perfil/defaultprofile.png")
        perfil.restaurant.add(mirestaurant)

    return mirestaurant

#FUNCION PARA AGREGAR O QUITAR UNA MESA DE LA VISTA "MESAS"
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def actualizar_mesas(request,operacion):
    mirestaurant = verificar_perfil(request)
    redirect_to = request.REQUEST.get('next', '')
    cantidad = Mesa.objects.filter(restaurant=mirestaurant).count()
    if operacion == "agregar":
        Mesa.objects.create(nombre=str(cantidad+1),restaurant=mirestaurant)
        return HttpResponseRedirect(redirect_to)
    elif operacion == "quitar":
        if cantidad > 0:
            mesa = Mesa.objects.latest('id')
            mesa.delete()
            return HttpResponseRedirect(redirect_to)
        else:
            return HttpResponseRedirect(redirect_to)
    else:
        return HttpResponseRedirect(redirect_to)

#FUNCION PARA ACTUALIZAR EL ESTADO DE UN PEDIDO A ENTRGADO, POR PARTE DE COCINA Y BAR
@login_required()
@user_passes_test(lambda u: u.groups.filter(name__in=["Cocina","Bar"]).count() > 0, login_url='/error/')
def actualizar_pedido(request,tipo,id_pedido):
    mirestaurant = verificar_perfil(request)
    redirect_to = request.REQUEST.get('next', '')
    
    if tipo == "plato":
        pedido = PedidoPlato.objects.get(id=id_pedido)
        pedido.estado = "entregado"
        pedido.save()
    elif tipo == "bebida":
        pedido = PedidoBebida.objects.get(id=id_pedido)
        pedido.estado = "entregado"
        pedido.save()

    return HttpResponseRedirect(redirect_to)

#VISTA PARA REALIZAR EL CAMBIO DE RESTAURANT, POR PARTE DE LOS USUARIOS ADMINISTRADORES
@login_required()
@user_passes_test(lambda u: u.groups.filter(name="Administradores").count() > 0, login_url='/fail/')
def cambiar_restaurant(request,id_restaurant):
    mirestaurant = verificar_perfil(request)
    mirestaurant.estado = "inactivo"
    mirestaurant.save()

    nuevo_restaurant = Restaurant.objects.get(id=id_restaurant)
    nuevo_restaurant.estado = "activo"
    nuevo_restaurant.save()

    redirect_to = request.REQUEST.get('next', '')

    return HttpResponseRedirect(redirect_to)


####################################################### CLIENTE ############################################################
