from django.contrib import admin
from .models import Medicine, Sale

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','price', 'quantity', 'expiry_date')
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'quantity', 'total_price', 'date_sold', 'sold_by')
    search_fields = ('medicine__name', 'sold_by__username')

