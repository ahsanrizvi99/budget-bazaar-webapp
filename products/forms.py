from django import forms
from .models import Product, Category

class ProductSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Product Name')
    quantity = forms.CharField(required=False, label='Quantity')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
