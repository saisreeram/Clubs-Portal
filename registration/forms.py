from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class Signup_form(UserCreationForm):
    #password=forms.CharField(widget=forms.PasswordInput())
    email=forms.EmailField()
    class Meta:
        model = User
        fields=['email','username','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if "@gmail.com" not in email:   # any check you need
            raise forms.ValidationError("Must be a gmail address")
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class AddProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender','ug']

class EditPasswordFrom(forms.Form):
    password=forms.CharField(label='Enter new password',widget=forms.PasswordInput(attrs={'placeholder':'Password*'}))
    confirm_password=forms.CharField(label='Re-enter the password',widget=forms.PasswordInput(attrs={'placeholder':'Retype Password*'}))
    class Meta:
        fields=('password','confirm_password')
