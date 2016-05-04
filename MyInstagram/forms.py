# coding="utf-8"

from django import forms
from MyInstagram.models import User, City

MIN_SIZE = 400
MAX_SIZE = 1080
MAX_PHOTO_SIZE = 1280


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    username = forms.CharField()
    password = forms.CharField(max_length=128,
                               strip=False,
                               widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, max_length=128)


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if self.fields[field].required:
                self.fields[field].label_suffix = "*:"

    confirm_password = forms.CharField(strip=False,
                                       widget=forms.PasswordInput)
    password = forms.CharField(min_length=6,
                               max_length=128,
                               strip=False,
                               widget=forms.PasswordInput)
    city = forms.CharField(max_length=City._meta.get_field('city').max_length,
                           required=False)
    next = forms.CharField(widget=forms.HiddenInput, max_length=128)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() != 0:
            raise forms.ValidationError(
                'Sorry, that username is taken.',
                code='invalid_username',
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() != 0:
            raise forms.ValidationError(
                'Sorry, that email is taken.',
                code='invalid_email',
            )

        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")
            self.add_error('password', "")


class NewPost(forms.Form):
    x1 = forms.IntegerField(widget=forms.HiddenInput, max_value=MAX_PHOTO_SIZE)
    x2 = forms.IntegerField(widget=forms.HiddenInput, max_value=MAX_PHOTO_SIZE)
    y1 = forms.IntegerField(widget=forms.HiddenInput, max_value=MAX_PHOTO_SIZE)
    y2 = forms.IntegerField(widget=forms.HiddenInput, max_value=MAX_PHOTO_SIZE)
    h = forms.IntegerField(widget=forms.HiddenInput, min_value=MIN_SIZE, max_value=MAX_SIZE)
    w = forms.IntegerField(widget=forms.HiddenInput, min_value=MIN_SIZE, max_value=MAX_SIZE)
    id = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super(NewPost, self).clean()
        x1 = cleaned_data.get('x1')
        y1 = cleaned_data.get('y1')
        x2 = cleaned_data.get('x2')
        y2 = cleaned_data.get('y2')
        h = cleaned_data.get('h')
        w = cleaned_data.get('w')
        if h != w:
            raise forms.ValidationError(
                'Width and height is not equal',
                code='invalid_h_w',
            )
        if x2 - x1 != w or y2 - y1 != h:
            raise forms.ValidationError(
                'Width or Height are not equal with x1, x2, y1, y2',
                code='invalid_coordinates',
            )