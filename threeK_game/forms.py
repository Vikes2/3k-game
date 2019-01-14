from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class LoginAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput({'class':'validate','placeholder': "Login"}),  label='')
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': "Hasło"}))