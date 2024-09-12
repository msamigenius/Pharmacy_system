from django.db import models
from django.contrib.auth.models import User

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500,default="No description available")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.name

class Sale(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()  # Make sure this is defined
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_sold = models.DateTimeField(auto_now_add=True)  # Make sure this is defined
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"Sale of {self.medicine.name} by {self.sold_by.username}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.medicine.price * self.quantity
        super().save(*args, **kwargs)



    @property
    def total_price(self):
        return self.medicine.price * self.quantity




class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order of {self.medicine.name} - {self.status}'

