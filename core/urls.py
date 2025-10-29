from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("api/uid/", views.uid_api, name="uid_api"),
    path('tables/', views.tables, name='tables'),
    path('account/', views.account_view, name='account'),
    path('api/client/', views.api_client_info, name='api_client'),
]