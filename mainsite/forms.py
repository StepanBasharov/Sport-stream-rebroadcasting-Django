from django.forms import Form
from django import forms
from django.contrib.auth.models import User


class LoginForm(Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'popup-reg__input_type_email popup-reg__form-styles', 'placeholder': 'login'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'popup-reg__input_type_password popup-reg__form-styles', 'placeholder': 'password'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'popup-reg__input_type_password popup-reg__form-styles', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'popup-reg__input_type_password popup-reg__form-styles', 'placeholder': 'Подтвержение пароля'}))

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
