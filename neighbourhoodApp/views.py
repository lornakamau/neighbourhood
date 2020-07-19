import folium
import random
import string
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/accounts/login/')
def email(request):
    current_user = request.user
    email = current_user.email
    name = current_user.username
    send_signup_email_admin(name, email)
    return redirect(create_profile_admin)

