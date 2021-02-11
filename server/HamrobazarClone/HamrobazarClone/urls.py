from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('Accounts.api.urls')),
    path('api/products/', include('Products.api.urls')),
    path('api/category/', include('Category.api.urls')),
]
