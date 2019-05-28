from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('nautilus/', include('nautilus.urls')),
    path('admin/', admin.site.urls),
    ]
