from django.shortcuts import render, redirect
from django.http import HttpResponse
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admins_only
# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            checked_group = request.POST.get('group')
            group = Group.objects.get(name=str(checked_group))
            # Customer.objects.create(user=user, name=user) # We done it in models.py BY signals
            user.groups.add(group)

            messages.success(
                request, "Account registered successfully: " + username)
            return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is Incorrect")
            return render(request, 'accounts/login.html', {'form': CreateUserForm()})
    return render(request, 'accounts/login.html', {'form': CreateUserForm()})


@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles='customer')
def userPage(request):
    orders = request.user.customer.order_set.all()
    orders_count = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'orders': orders, 'orders_count': orders_count,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@admins_only
def home(request):
    customers = Customer.objects.all().order_by('date_created')
    orders = Order.objects.all().order_by('-date_created')
    customers_count = customers.count()
    orders_count = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'customers': customers, 'orders': orders, 'customers_count': customers_count,
               'orders_count': orders_count, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    return render(request, 'accounts/products.html', {'products': Product.objects.all()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all().order_by('-date_created')
    orders_count = orders.count()

    myFilter = OrderFilter(request.POST, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'orders_count': orders_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    if pk == 'add':
        form = OrderForm()
    else:
        customer = Customer.objects.get(id=pk)
        form = OrderForm(initial={'customer': customer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete_confirm.html', context)
