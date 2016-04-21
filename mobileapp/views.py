# coding: utf-8
#ARCHIVO PARA CONFIGURACION DE VISTAS Y FUNCIONES
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
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

#FUNCION PARA LA REDIRECCION DE USUARIOS CON UNA SESION ABIERTA O LA SOLICITUD DE LOGIN
def control_ingreso_cliente(request,id_mesa):
    if not request.user.is_authenticated():
        url = reverse('login_cliente', kwargs={'id_mesa': id_mesa})
        return HttpResponseRedirect(url)
    else:
        url = reverse('home_cliente', kwargs={'id_mesa': id_mesa})
        return HttpResponseRedirect(url)

#FUNCION DE LOGIN DEL CLIENTE
def login_cliente(request,id_mesa):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                url = reverse('home_cliente', kwargs={'id_mesa': id_mesa})
                return HttpResponseRedirect(url)

    mesa = Mesa.objects.get(id=id_mesa)
    ctx = {"mesa":mesa}
    
    return render_to_response('mobileapp/login.html',ctx, context_instance=RequestContext(request))

#VISTA DE LOS 4 BOTONES DE LA APLICACION
def home(request,id_mesa):
    mesa = Mesa.objects.get(id=id_mesa)
    ctx = {"mesa":mesa}

    return render_to_response('mobileapp/home.html', ctx, context_instance=RequestContext(request))

#FUNCION PARA LA CREACION DE NUEVO USUARIO
def nuevo_usuario_cliente(request,id_mesa):
    if request.method=='POST':
        formulario_user = UserCreationForm(request.POST)

        if formulario_user.is_valid():
            user = formulario_user.save()
            clientes = Group.objects.get(name='Clientes') 
            clientes.user_set.add(user)

            url = reverse('login_cliente', kwargs={'id_mesa': id_mesa})
            return HttpResponseRedirect(url)
    else:
        formulario_user = UserCreationForm()
    return render_to_response('mobileapp/nuevousuario.html',{'formulario_user':formulario_user},context_instance=RequestContext(request))

#FUNCION PARA CERRAR SESION
def logout_cliente(request):
    logout(request)
    url = reverse('error_cliente', kwargs={})
    return HttpResponseRedirect(url)

#FUNCION PARA NO PERMITIR EL INGRESO A LOS USUARIOS NO REGISTRADOS
def error_cliente(request):
    redirect_to = None
    try:
        redirect_to = request.REQUEST.get('next', '')
    except Informetecnicocorrectivo.DoesNotExist:
        redirect_to = None

    ctx = {'redirect_to':redirect_to}

    return render_to_response('mobileapp/error.html',ctx,context_instance=RequestContext(request))

#VISTA DEL MENU
def menu(request,id_mesa):
    mesa = Mesa.objects.get(id=id_mesa)
    platos = Plato.objects.filter(restaurant=mesa.restaurant)
    pedidosplato = PedidoPlato.objects.filter(mesa=mesa,estado="pedido",cliente=request.user).exclude(estado="cuenta")
    bebidas = Bebida.objects.filter(restaurant=mesa.restaurant)
    pedidosbebida = PedidoBebida.objects.filter(mesa=mesa,estado="pedido",cliente=request.user).exclude(estado="cuenta")

    form = CantidadForm()

    ctx = {"mesa":mesa,"platos":platos,"pedidosplato":pedidosplato,"bebidas":bebidas,"pedidosbebida":pedidosbebida,'form':form}

    return render_to_response('mobileapp/menu.html', ctx, context_instance=RequestContext(request))

#VISTA DE LA CUENTA TOTAL POR MESA 
def cuentatotal(request,id_mesa):
    mesa = Mesa.objects.get(id=id_mesa)
    pedidosplato = PedidoPlato.objects.filter(mesa=mesa,estado="entregado")
    pedidosbebida = PedidoBebida.objects.filter(mesa=mesa,estado="entregado")

    costototal = 0

    for pplato in pedidosplato:
        costototal = costototal + (pplato.cantidad * pplato.plato.precio) 

    for pbebida in pedidosbebida:
        costototal = costototal + (pbebida.cantidad * pbebida.bebida.precio) 

    ctx = {"mesa":mesa,"pedidosplato":pedidosplato,"pedidosbebida":pedidosbebida,'costototal':costototal}

    return render_to_response('mobileapp/cuentatotal.html', ctx, context_instance=RequestContext(request))

#VISTA DE LA CUENTA PROPIA DEL CLIENTE
def cuentapropia(request,id_mesa):
    mesa = Mesa.objects.get(id=id_mesa)
    pedidosplato = PedidoPlato.objects.filter(mesa=mesa,cliente=request.user,estado="entregado")
    pedidosbebida = PedidoBebida.objects.filter(mesa=mesa,cliente=request.user,estado="entregado")

    costototal = 0

    for pplato in pedidosplato:
        costototal = costototal + (pplato.cantidad * pplato.plato.precio) 

    for pbebida in pedidosbebida:
        costototal = costototal + (pbebida.cantidad * pbebida.bebida.precio) 

    ctx = {"mesa":mesa,"pedidosplato":pedidosplato,"pedidosbebida":pedidosbebida,'costototal':costototal}

    return render_to_response('mobileapp/cuentapropia.html', ctx, context_instance=RequestContext(request))

#FUNCION PARA CREAR UN NUEVO PEDIDO DE PLATO O BEBIDA
def pedido(request,tipo,id_mesa,id_elemento):
    redirect_to = request.REQUEST.get('next', '')
    mesa = Mesa.objects.get(id=id_mesa)

    micantidad = 1
    form = CantidadForm(request.POST)
    if form.is_valid():
        micantidad = form.cleaned_data['cantidad']

    if tipo == "plato":
        plato = Plato.objects.get(id=id_elemento)

        nuevopedido = PedidoPlato.objects.create(mesa=mesa,cliente=request.user,plato=plato,estado="pedido",cantidad=micantidad)
    elif tipo == "bebida":
        bebida = Bebida.objects.get(id=id_elemento)
        nuevopedido = PedidoBebida.objects.create(mesa=mesa,cliente=request.user,bebida=bebida,estado="pedido",cantidad=micantidad)

    return HttpResponseRedirect(redirect_to)

#FUNCION PARA CANCELAR UN PEDIDO DE PLATO O BEBIDA
def cancelar(request,tipo,id_pedido):
    redirect_to = request.REQUEST.get('next', '')

    if tipo == "plato":
        pedido = PedidoPlato.objects.get(id=id_pedido)
        pedido.delete()

    elif tipo == "bebida":
        pedido = PedidoBebida.objects.get(id=id_pedido)
        pedido.delete()

    return HttpResponseRedirect(redirect_to)

#FUNCION PARA PEDIR LA CUENTA Y CAMBIAR EL ESTADO DE LOS PEDIDOS A CUENTA
def pedircuenta(request,id_mesa):
    mesa = Mesa.objects.get(id=id_mesa)
    pedidosplato = PedidoPlato.objects.filter(mesa=mesa,cliente=request.user,estado="entregado")
    pedidosbebida = PedidoBebida.objects.filter(mesa=mesa,cliente=request.user,estado="entregado")

    for p in pedidosplato:
        p.estado = "cuenta"
        p.save()

    for p in pedidosbebida:
        p.estado = "cuenta"
        p.save()

    url = reverse('home_cliente', kwargs={'id_mesa': id_mesa})
    return HttpResponseRedirect(url)

#FUNCION PARA PEDIR ALGUN ITEM EXTRA A LOS PLATOS Y BEBIDAS
def pedidoextra(request,id_mesa):
    mesa = Mesa.objects.get(id=id_mesa)
    info = False
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = PedidoExtraForm(request.POST, request.FILES) 
        if form.is_valid():
            registro = form.save()
            info = True
        else:
            form.fields['mesa'].widget = forms.HiddenInput()
            form.fields['cliente'].widget = forms.HiddenInput()
            form.fields['estado'].widget = forms.HiddenInput()
    else:
        form = PedidoExtraForm(initial={'mesa':mesa,'cliente':request.user,'estado':"pedido"})
        form.fields['mesa'].widget = forms.HiddenInput()
        form.fields['cliente'].widget = forms.HiddenInput()
        form.fields['estado'].widget = forms.HiddenInput()

    ctx = {'form':form,'redirect_to':redirect_to,'info':info,'mesa':mesa}
    return render_to_response('mobileapp/pedidoextra.html',ctx,context_instance=RequestContext(request))

#VISTA DE RECOMENDACIONES DEL RESTAURANT, CAMARERO O CONSUMO
def recomendaciones(request,id_mesa):
    mesa = Mesa.objects.get(id=id_mesa)
    restaurant = Restaurant.objects.get(id=mesa.restaurant.id)
    if request.method=='POST':
        form1 = RecomendacionRestaurantForm(request.POST)
        form2 = RecomendacionCamareroForm(request.POST)
        form3 = RecomendacionConsumoForm(request.POST)
        

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            form3.save()

            url = reverse('home_cliente', kwargs={'id_mesa': id_mesa})
            return HttpResponseRedirect(url)
        else:
            form1.fields['restaurant'].widget = forms.HiddenInput()
            form2.fields['restaurant'].widget = forms.HiddenInput()
            form3.fields['restaurant'].widget = forms.HiddenInput()
            form1.fields['cliente'].widget = forms.HiddenInput()
            form2.fields['cliente'].widget = forms.HiddenInput()
            form3.fields['cliente'].widget = forms.HiddenInput()
    else:
        form1 = RecomendacionRestaurantForm(initial={'restaurant':restaurant,'cliente':request.user})
        form2 = RecomendacionCamareroForm(initial={'restaurant':restaurant,'cliente':request.user})
        form3 = RecomendacionConsumoForm(initial={'restaurant':restaurant,'cliente':request.user})
        form1.fields['restaurant'].widget = forms.HiddenInput()
        form2.fields['restaurant'].widget = forms.HiddenInput()
        form3.fields['restaurant'].widget = forms.HiddenInput()
        form1.fields['cliente'].widget = forms.HiddenInput()
        form2.fields['cliente'].widget = forms.HiddenInput()
        form3.fields['cliente'].widget = forms.HiddenInput()
        
    return render_to_response('mobileapp/recomendaciones.html',{'form1':form1,'form2':form2,'form3':form3,'mesa':mesa},context_instance=RequestContext(request))