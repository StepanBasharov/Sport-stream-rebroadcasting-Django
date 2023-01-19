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
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "popup-reg__input_type_name popup-reg__form-styles",
                'placeholder': 'Имя'
            }),
            'email': forms.TextInput(attrs={
                'class': "popup-reg__input_type_password popup-reg__form-styles",
                'placeholder': 'email',
                'type': 'email'
            })
        }

    def clean_password2(self):
        obscene_words = [
            'хуй',
            'пизда',
            'уебок',
            'ебать',
            'Говно', 'залупа', 'пенис', 'хер', 'давалка', 'хyй', 'блядина', 'шлюха', 'жопа', 'член', 'еблан', 'петух',
            'мудила',
            'Рукоблуд', 'ссанина', 'очко', 'блядун', 'вагина', 'Сука', 'ебланище', 'влагалище', 'пердун', 'дрочила',
            'Пидор', 'пи3да',
            'гомик', 'мудила', 'пилотка', 'манда', 'Анус', 'вагина', 'путана', 'педрила', 'шалава', 'хуила', 'мошонка',
            'елда'
        ]
        cd = self.cleaned_data
        if cd['password'] != cd['password2'] or cd['password'] == cd['username'] or cd['password'] == cd['email']:
            raise forms.ValidationError('Passwords don\'t match.')
        for word in obscene_words:
            if word in cd['username'].lower():
                raise forms.ValidationError("obscene words")
        return cd['password2']


class NewsCommetnsForm(forms.ModelForm):
    pass
