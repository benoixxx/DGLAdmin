from django import forms
from django.forms import PasswordInput


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=PasswordInput())


class UserForm(forms.Form):
    firstName = forms.CharField(max_length=50)
    lastName = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=PasswordInput())


class FestivalForm(forms.Form):
    name = forms.CharField(max_length=100)
    street = forms.CharField(max_length=100)
    locality = forms.CharField(max_length=50)
    city = forms.CharField(max_length=100)
    region = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    startDate = forms.CharField(max_length=10)
    endDate = forms.CharField(max_length=10)
    email = forms.CharField(max_length=100)


TYPES_CHOICES = (('Stage', 'Stage'), ('Bar', 'Bar'), ('WC', 'WC'), ('Camping', 'Camping'),
                 ('Infirmary', 'Infirmary'), ('Restaurant', 'Restaurant'))


class PoiForm(forms.Form):
    name = forms.CharField(max_length=100)
    lat = forms.CharField(max_length=100)
    long = forms.CharField(max_length=100)
    category = forms.ChoiceField(choices=TYPES_CHOICES, required=True)


class ArtistForm(forms.Form):
    name = forms.CharField(max_length=100)
    startDate = forms.CharField(max_length=16)
    endDate = forms.CharField(max_length=16)


