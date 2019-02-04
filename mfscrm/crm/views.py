from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Sum
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .utils import *

now = timezone.now()
def home(request):
   return render(request, 'crm/home.html',
                 {'crm': home})

@login_required
def customer_list(request, pk):
    if pk == 0:
        customer = Customer.objects.filter(created_date__lte=timezone.now())
        action = ""
        return render(request, 'crm/customer_list.html', {'customers': customer, 'action': action})
    else:
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        action = "deleted"
        customers = Customer.objects.filter(created_date__lte=timezone.now())
        return render(request, 'crm/customer_list.html', {'customers': customers, 'action': action})

@login_required
def customer_new(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           customers = Customer.objects.filter(created_date__lte=timezone.now())
           action = "added"
           return render(request, 'crm/customer_list.html',
                         {'customers': customers, 'action': action})
   else:
       form = CustomerForm()
       # print("Else")
   return render(request, 'crm/customer_new.html', {'form': form})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           action = "edited"
           return render(request, 'crm/customer_list.html',
                         {'customers': customer, 'action': action})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'crm/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   action = "deleted"
   return redirect('crm:customer_list')

@login_required
def service_list(request, pk):
    if pk == 0:
        services = Service.objects.filter(created_date__lte=timezone.now())
        action = ""
        return render(request, 'crm/service_list.html', {'services': services, 'action': action})
    else:
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        action = "deleted"
        services = Service.objects.filter(created_date__lte=timezone.now())
        return render(request, 'crm/service_list.html', {'services': services, 'action': action})
@login_required
def service_new(request):
   if request.method == "POST":
       form = ServiceForm(request.POST)
       if form.is_valid():
           service = form.save(commit=False)
           service.created_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           action = "added"
           return render(request, 'crm/service_list.html',
                         {'services': services, 'action': action})
   else:
       form = ServiceForm()
       # print("Else")
   return render(request, 'crm/service_new.html', {'form': form})

@login_required
def service_edit(request, pk):
   service = get_object_or_404(Service, pk=pk)
   if request.method == "POST":
       form = ServiceForm(request.POST, instance=service)
       if form.is_valid():
           service = form.save()
           # service.customer = service.id
           service.updated_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           action = "edited"
           return render(request, 'crm/service_list.html', {'services': services, 'action': action})
   else:
       # print("else")
       form = ServiceForm(instance=service)
   return render(request, 'crm/service_edit.html', {'form': form})

@login_required
def product_list(request, pk):
   if pk == 0:
        products = Product.objects.filter(created_date__lte=timezone.now())
        action = ""
        return render(request, 'crm/product_list.html', {'products': products, 'action': action})
   else:
       product = get_object_or_404(Product, pk=pk)
       product.delete()
       action = "deleted"
       products = Product.objects.filter(created_date__lte=timezone.now())
       return render(request, 'crm/product_list.html', {'products': products, 'action': action})

@login_required
def product_new(request):
   if request.method == "POST":
       form = ProductForm(request.POST)
       if form.is_valid():
           product = form.save(commit=False)
           product.created_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           action = "added"
           return render(request, 'crm/product_list.html',
                         {'products': products, 'action': action})
   else:
       form = ProductForm()
       # print("Else")
   return render(request, 'crm/product_new.html', {'form': form})

@login_required
def product_edit(request, pk):
   product = get_object_or_404(Product, pk=pk)
   if request.method == "POST":
       form = ProductForm(request.POST, instance=product)
       if form.is_valid():
           product = form.save()
           # service.customer = service.id
           product.updated_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           action = "edited"
           return render(request, 'crm/product_list.html', {'products': products, 'action': action})
   else:
       # print("else")
       form = ProductForm(instance=product)
   return render(request, 'crm/product_edit.html', {'form': form})

@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    customers = Customer.objects.filter(cust_name=pk)
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    sum_of_totals = Sum(sum_service_charge, sum_product_charge)
    return render(request, 'crm/summary.html', {'customer': customer,
                                                    'products': products,
                                                    'services': services,
                                                    'sum_service_charge': sum_service_charge,
                                                    'sum_product_charge': sum_product_charge,
                                                    'sum_of_totals': sum_of_totals,})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'crm/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'crm/register.html',
                  {'user_form': user_form})

def customer_summary_pdf(request, pk):
        template = get_template('report/customer_summary_pdf.html')
        customer = get_object_or_404(Customer, pk=pk)
        customers = Customer.objects.filter(created_date__lte=timezone.now())
        customers = Customer.objects.filter(cust_name=pk)
        services = Service.objects.filter(cust_name=pk)
        products = Product.objects.filter(cust_name=pk)
        sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
        sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
        data = {
                'customer': customer,
                'products': products,
                'services': services,
                'sum_service_charge': sum_service_charge,
                'sum_product_charge': sum_product_charge,
        }
        pdf = render_to_pdf('report/customer_summary_pdf.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Summary_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
            return HttpResponse("Not found")

        return HttpResponse(pdf, content_type='application/pdf')