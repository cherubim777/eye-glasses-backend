from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views


urlpatterns = [path("salesReport/", views.GetSalesReport.as_view(), name="salesReport")]
