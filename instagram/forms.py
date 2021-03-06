from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class NewUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'user', 'bio')


class PostForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ['image', 'name', 'caption']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']