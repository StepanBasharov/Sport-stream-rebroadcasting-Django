from django.forms import Form
from django import forms


class LoginForm(Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'popup-reg__input_type_email popup-reg__form-styles', 'placeholder': 'login'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'popup-reg__input_type_password popup-reg__form-styles', 'placeholder': 'password'}))
