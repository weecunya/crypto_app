from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserInfo

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'first_name', 'last_name')
