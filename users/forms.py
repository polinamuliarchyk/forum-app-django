from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.views import LogoutView


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(required=True, help_text='Required. Inform a valid username.',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               label='Username')
    password = forms.CharField(required=True, help_text='Required. Inform a valid password.',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               label='Password')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
