from django import forms
from .models import Product, Order
from django.contrib.auth.models import Group
from django.forms import ModelForm

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'discription', 'price', 'discount'


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promo_code', 'products', 'user'