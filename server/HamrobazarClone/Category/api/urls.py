from django.urls import path
from . import views

urlpatterns = [
    path('',views.api_caregories_view),
    path('<int:pk>',views.api_single_category_view),
    path('new',views.api_add_category_view),
    path('update/<int:pk>',views.api_update_category_view),
    path('delete/<int:pk>',views.api_delete_category_view),
]
