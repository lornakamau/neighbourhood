from django import forms
from .models import Admin, Neighbourhood

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['user']


class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ['admin', 'occupants']


class AddResidentForm(forms.Form):
    name = forms.CharField(label='Resident name', max_length=50)
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField()  