from django.shortcuts import render,redirect

from django.http import HttpResponse

from django.forms import inlineformset_factory

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from accounts.forms import *

from accounts.models import *

from accounts.filters import OrderFilter

from accounts.decorators import unauthenticated_user,allowed_users,admin_only



@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for '+ username)
            return redirect('login')

    context = {'form':form}

    return render(request,'accounts/register.html',context)



@unauthenticated_user
def loginPage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username = username,password = password)

            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return render(request,'accounts/login.html')

        return render(request,'accounts/login.html')

def logOut(request):
    logout(request)

    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers':customers, 'orders':orders,
    'total_orders':total_orders,'delivered':delivered, 'pending':pending}

    return render(request,'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()



    context = {'orders':orders,'total_orders':total_orders,
               'delivered':delivered, 'pending':pending}
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    total_orders = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)

    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'total_orders':total_orders,
               'myFilter':myFilter}


    return render(request,'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})


#create
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('products','status'), extra=5)

    customer = Customer.objects.get(id = pk)

    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)

    #form = OrderForm(initial={'customer':customer})
    

    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        
    context = {'formset':formset}


    return render(request,'accounts/order_form_cus.html',context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def createCustomer(request):
    
#     form = CustomerForm()

#     context = {'form':form}

#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid:
#             form.save()
#             return redirect('/')

#     return render(request,'accounts/customer_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)
    context = {'form':form}

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')


    return render(request,'accounts/order_form.html',context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def updateCustomer(request,pk):
#     customer = Customer.objects.get(id = pk)
#     form = CustomerForm(instance = customer)

#     context = {'form':form}

#     if request.method == 'POST':
#         form = CustomerForm(request.POST,instance = customer)
#         if form.is_valid:
#             form.save()
#             return redirect('/')

#     return render(request,'accounts/customer_form.html',context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):

    order = Order.objects.get(id = pk)

    context = {'item':order}

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    
    return render(request,'accounts/order_delete.html',context)



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def deleteCustomer(request,pk):

#     customer = Customer.objects.get(id = pk)

#     context = {'customer':customer}

#     if request.method == 'POST':
#         customer.delete()
#         return redirect('/')

    
#     return render(request,'accounts/customer_delete.html',context)

