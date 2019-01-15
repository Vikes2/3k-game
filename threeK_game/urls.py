
#from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views
from threeK_game.forms import LoginAuthForm, RegisterForm

app_name='three_k'
urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('game/', views.game),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginAuthForm, template_name = 'registration/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    # re_path(r'^signup/$', views.signup, name='signup'),
    path('signup/', views.signup, name='signup')
]