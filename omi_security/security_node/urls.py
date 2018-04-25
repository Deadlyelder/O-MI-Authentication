from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'login', views.login, name='login'),
]

