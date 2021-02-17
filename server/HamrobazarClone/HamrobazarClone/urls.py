from django.contrib import admin
from django.urls import path,include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('Accounts.api.urls')),
    path('api/products/', include('Products.api.urls')),
    path('api/categories/', include('Category.api.urls')),

   path('docs/',include_docs_urls(title="Hamrobazar Clone")),
   path('schema', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
]
