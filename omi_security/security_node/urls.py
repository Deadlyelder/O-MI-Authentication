from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'login', views.login, name='login'),
    path(r'signup', views.signup, name='signup'),
    path(r'logout', views.logout, name='logout'),
    path(r'authmodule', views.authmodule, name='authmodule'),
    path(r'omi_authquery', views.omi_authquery, name='omi_authquery'),
    path(r'about', views.about, name='about'),


]

