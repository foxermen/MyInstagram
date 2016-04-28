# coding="utf-8"

from django import forms
from MyInstagram.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               min_length=1,
                               help_text="Required. 30 characters or fewer. Letters, digits and @.+-_")
    password = forms.CharField(min_length=8,
                               max_length=128,
                               strip=False,
                               help_text="Required. 8 characters or more",
                               widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, max_length=128)


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(min_length=8,
                                       max_length=128,
                                       strip=False,
                                       widget=forms.PasswordInput)
    password = forms.CharField(min_length=8,
                               max_length=128,
                               strip=False,
                               help_text="Required. 8 characters or more",
                               widget=forms.PasswordInput)
    city = forms.CharField(required=False)
    next = forms.CharField(widget=forms.HiddenInput, max_length=128)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class NewPostForm(forms.Form):
    photo = forms.ImageField()