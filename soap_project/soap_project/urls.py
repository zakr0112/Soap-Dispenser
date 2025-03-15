"""
URL configuration for soap_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from dispenser.views import home, shifts, stock, sites, dispenser_resolved, get_collection_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('shifts/', shifts, name='shifts'),
    path('stock/', stock, name='stock'),
    path('sites/', sites, name='sites'),
    path('dispenserlist/', dispenser_resolved, name='dispenser_resolved'),
    path('get_collection_data/<str:dispenser_id>/', get_collection_data, name='get_collection_data'),
]