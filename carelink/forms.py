from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
      username = forms.CharField(
        label="Username",
        strip=False,
        help_text="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        )
      password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text="",
        )
      password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}),
        strip=False,
        help_text="",
          )


class Meta:
    model = User
    fields = ['username','email','password1','password2']


class LoginForm  (AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

