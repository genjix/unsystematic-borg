from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from unsystem.models import UserProfile

class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Re-enter password", widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already taken!")

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match!")
        return password2

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile

