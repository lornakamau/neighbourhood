from django import forms
from .models import Admin, Neighbourhood, Occupant, Business, Post, Amenity

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['user']


class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ['admin', 'occupants']


class AddResidentForm(forms.Form):
    name = forms.CharField(label='Occupant name', max_length=50)
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField()  

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        exclude = ['created', 'neighbourhood']

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['neighbourhood']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['occupant', 'post_date', 'neighbourhood']