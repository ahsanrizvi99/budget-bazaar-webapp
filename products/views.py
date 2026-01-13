
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductSearchForm

def product_list(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        quantity = form.cleaned_data.get('quantity')
        category = form.cleaned_data.get('category')

        if name:
            products = products.filter(name__icontains=name)
        if quantity:
            products = products.filter(quantity__icontains=quantity)
        if category:
            products = products.filter(category=category)

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'product_list.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('product_list')

def product_search(request):
    if request.method == 'GET':
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            quantity = form.cleaned_data.get('quantity')
            category = form.cleaned_data.get('category')

            products = Product.objects.all()

            if name:
                products = products.filter(name__icontains=name)
            if quantity:
                products = products.filter(quantity__icontains=quantity)
            if category:
                products = products.filter(category=category)

            cheapest_product = None
            cheapest_price = None
            for product in products:
                if cheapest_product is None or product.price < cheapest_price:
                    cheapest_product = product
                    cheapest_price = product.price

            context = {
                'search_results': products,
                'cheapest_product': cheapest_product,
            }

            if not products:  
                context['no_items_found'] = True

            return render(request, 'product_search_results.html', context)
        else:
            return render(request, 'product_search_results.html', {'error': 'Please provide valid search criteria.'})
    else:
        return redirect('product_list') 
