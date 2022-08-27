from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {'email' : 'Email', 'first_name' : 'First Name', 'last_name' : 'Last Name', 'password2':'Confirm Password'}


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['photo']
        labels = {'photo':'Upload Image'}
