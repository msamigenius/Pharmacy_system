from django import forms
from .models import Medicine, Sale , Order

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name','description', 'price', 'quantity', 'expiry_date']



class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['medicine', 'quantity']  # Use the correct field names from the Sale model


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['medicine', 'quantity', 'status']
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES),
        }
