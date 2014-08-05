# -*- encoding: utf8 -*-
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label='Login')
    password = forms.CharField(max_length=32, label=u'Hasło', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=100, label='Login')
    email = forms.EmailField()
    password = forms.CharField(max_length=32, label='Haslo', widget=forms.PasswordInput)
    verify = forms.CharField(max_length=100, label=u'Stolica Polski:')