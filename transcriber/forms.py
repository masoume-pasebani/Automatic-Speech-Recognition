# transcriber/forms.py
from django import forms
from .models import Transcription
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class TranscriptionForm(forms.ModelForm):
    class Meta:
        model = Transcription
        fields = ['audio_file']


User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control",
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "form-control",
            }
        ))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "First Name",
                "class": "form-control",
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Last Name",
                "class": "form-control",
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control",
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",
                "class": "form-control",
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "form-control",
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm Password",
                "class": "form-control",
            }
        ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')