from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.forms.widgets import PasswordInput, TextInput


class LoginAuthForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control', 'placeholder':"Nazwa użytkownika"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Hasło"}),
    )

class RegisterForm(UserCreationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control', 'placeholder':"Nazwa użytkownika"}))
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Hasło"}),
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Powtórz hasło"}),
    )