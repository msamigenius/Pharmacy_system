from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),
#     path('manage-medicine/', views.manage_medicine, name='manage_medicine'),
#     path('add-medicine/', views.add_medicine, name='add_medicine'),
#     path('edit-medicine/<int:pk>/', views.edit_medicine, name='edit_medicine'),
#     path('delete-medicine/<int:pk>/', views.delete_medicine, name='delete_medicine'),
#     path('process-sale/', views.process_sale, name='process_sale'),
#     path('report/', views.report, name='report'),
#     path('inventory/', views.inventory, name='inventory'),
# ]


# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage-medicine/', views.manage_medicine, name='manage_medicine'),
    path('add-medicine/', views.add_medicine, name='add_medicine'),
    path('edit-medicine/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('delete-medicine/<int:pk>/', views.delete_medicine, name='delete_medicine'),
    path('process-sale/', views.process_sale, name='process_sale'),
    path('report/', views.report, name='report'),
    path('inventory/', views.inventory, name='inventory'),
    path('order-management/', views.order_management, name='order_management'),
    path('add-order/', views.add_order, name='add_order'),
    path('edit-order/<int:pk>/', views.update_order, name='update_order'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete_order'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
