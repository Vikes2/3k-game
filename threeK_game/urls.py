
#from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name='three_k'
urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('game/', views.game),
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^signup/$', views.signup, name='signup'),
]