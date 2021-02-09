from django.urls import path
from . import views

urlpatterns = [
    path('',views.api_products_view),
    path('new',views.api_add_product_view),
    path('update/<int:pk>',views.api_update_product_view),
    path('delete/<int:pk>',views.api_delete_product_view),
]
