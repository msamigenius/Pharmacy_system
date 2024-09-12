from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Medicine, Sale
from .forms import MedicineForm , SaleForm
from django.shortcuts import render, redirect
from .models import Sale, Medicine
from .forms import SaleForm
from django.contrib.auth.decorators import login_required
# @login_required
# def dashboard(request):
#     return render(request, 'pharma/dashboard.html')

from django.db.models import Sum,  F, FloatField
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Cast

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'pharma/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Calculate total number of medicines
    total_medicines = Medicine.objects.count()
    orders = Order.objects.count()


    # Calculate total sales dynamically
    total_sales = Sale.objects.annotate(
        sale_total=Cast(F('quantity') * F('medicine__price'), FloatField())
    ).aggregate(total_sales=Sum('sale_total'))['total_sales'] or 0

    # Calculate pending orders (assuming 'pending' is a status in your Sale model)
    pending_orders = Order.objects.filter(status='pending').count()
    orders = Order.objects.exclude(status='Completed')

    context = {
        'total_medicines': total_medicines,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
        'orders': orders
    }

    return render(request, 'pharma/dashboard.html', context)

@login_required
def manage_medicine(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharma/manage_medicine.html', {'medicines': medicines})

@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = MedicineForm()
    return render(request, 'pharma/add_medicine.html', {'form': form})

@login_required
def edit_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('manage_medicine')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'pharma/edit_medicine.html', {'form': form})

@login_required
def delete_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    medicine.delete()
    return redirect('manage_medicine')



@login_required
def process_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            # Calculate the total price based on the quantity and medicine price
            # sale.total_price = sale.medicine.price * sale.quantity
            sale.sold_by = request.user
            sale.save()

            # Update the quantity of the medicine in stock
            medicine = sale.medicine
            medicine.quantity -= sale.quantity
            medicine.save()

            return redirect('report')  # Redirect to inventory after sale
    else:
        form = SaleForm()

    return render(request, 'pharma/process_sale.html', {'form': form})


@login_required
def report(request):
    sales = Sale.objects.all()
    return render(request, 'pharma/report.html', {'sales': sales})

@login_required
def inventory(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharma/inventory.html', {'medicines': medicines})









# pharma/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Medicine
from .forms import OrderForm

@login_required
def order_management(request):
    orders = Order.objects.all()
    return render(request, 'pharma/order_management.html', {'orders': orders})

@login_required
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_management')
    else:
        form = OrderForm()
    return render(request, 'pharma/add_order.html', {'form': form})

@login_required
def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_management')
    else:
        form = OrderForm(instance=order)
    return render(request, 'pharma/edit_order.html', {'form': form})

@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_management')
    return render(request, 'pharma/delete_order.html', {'order': order})



# pharma/views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.status = 'Completed'
        order.save()
        print("yes")
        # medicines = Medicine.objects.exclude(id=excluded_id)
        return redirect('dashboard')
    return JsonResponse({'status': 'error'}, status=400)


