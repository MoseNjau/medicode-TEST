from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import User_profile

class CreateUserForm(UserCreationForm):
    id_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Number'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    
    class Meta:
        model = User
        fields = ['username', 'id_number','phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control text-default', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.id_number = self.cleaned_data['id_number']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user
    



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))


    

# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User_profile

class ProfileForm(forms.ModelForm):
    id_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Number'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    
    class Meta:
        model = User_profile
        fields = ['id_number', 'phone_number']

