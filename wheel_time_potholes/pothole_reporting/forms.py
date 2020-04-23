from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms.widgets import PasswordInput, TextInput


class PotholeImageForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg'])],
                           widget=forms.FileInput(attrs={'accept': 'image/jpeg'}),
                           label="Select Pothole image")


class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


class SignupForm(forms.Form):
    username = forms.CharField(label='',widget=forms.TextInput(attrs={"placeholder" : "Username"}))
    first_name = forms.CharField(label='',widget=forms.TextInput(attrs={"placeholder" : "Firstname"}))
    last_name = forms.CharField(label='',widget=forms.TextInput(attrs={"placeholder" : "Lastname"}))
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={"placeholder" : "Email"}))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={"placeholder" : "Enter password"}))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={"placeholder" : "Re-enter password"}))
