# coding=utf-8
# REGISTRO DE LOS FORMULARIOS DE LA APLICACION WEB

from django.forms import ModelForm
from webapp.models import *
from django import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django.views.generic.edit import UpdateView
from django.template.loader import render_to_string
from datetime import date
from django.core.exceptions import ValidationError


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        exclude=['user','restaurant']

class RestaurantForm(forms.ModelForm):
    hidden_redirect = forms.CharField(widget=forms.HiddenInput(),initial="/restaurantes/")
    class Meta:
        model = Restaurant

class BebidaForm(forms.ModelForm):
    hidden_redirect = forms.CharField(widget=forms.HiddenInput(),initial="/bebidas/")
    class Meta:
        model = Bebida

class PlatoForm(forms.ModelForm):
    hidden_redirect = forms.CharField(widget=forms.HiddenInput(),initial="/platos/")
    class Meta:
        model = Plato


class UserForm(forms.ModelForm):
	hidden_redirect = forms.CharField(widget=forms.HiddenInput(),initial="/personal/")
	class Meta:
		model = User
		fields = ('first_name','last_name','username','email', 'groups',  )

class MiUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class CategoriaForm(forms.ModelForm):
    hidden_redirect = forms.CharField(widget=forms.HiddenInput(),initial="/categorias/")
    class Meta:
        model = Categoria

class CantidadForm(forms.Form):
    cantidad = forms.IntegerField(initial=1,min_value=1)

class PedidoExtraForm(forms.ModelForm):
    class Meta:
        model = PedidoExtra

class RecomendacionRestaurantForm(forms.ModelForm):
    class Meta:
        model = RecomendacionRestaurant

class RecomendacionCamareroForm(forms.ModelForm):
    class Meta:
        model = RecomendacionCamarero

class RecomendacionConsumoForm(forms.ModelForm):
    class Meta:
        model = RecomendacionConsumo