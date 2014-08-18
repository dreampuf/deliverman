from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

class AccountsAuthentcationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={"class" : "form-control"}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={"class" : "form-control"}))
