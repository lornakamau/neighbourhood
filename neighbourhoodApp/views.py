import folium
import random
import string
from django.shortcuts import render, redirect
from .models import Neighbourhood, Admin, Occupant, Business, Amenity, Post
from django.contrib.auth.decorators import login_required
from .forms import AdminProfileForm, NeighbourhoodForm, AddResidentForm

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/accounts/login/')
def email(request):
    current_user = request.user
    email = current_user.email
    name = current_user.username
    send_signup_email_admin(name, email)
    return redirect(create_profile_admin)

@login_required(login_url='/accounts/login/')
def create_profile_admin(request):
    current_user = request.user
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.this_user = current_user
            profile.save()
        return redirect(create_hood)

    else:
        form = AdminProfileForm()
      
    title = "Admin profile "
    return render(request, 'create-profile-admin.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def create_hood(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()

    my_hood = None
    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        pass

    if my_hood:
        return redirect(my_admin_profile)

    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = admin_profile
            hood.save()
        return redirect(my_admin_profile)

    else:
        form = NeighbourhoodForm()
      
    title = "Create Hood"
    return render(request, 'create-hood.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def my_admin_profile(request):
    current_user = request.user
    try:
        admin_profile = Admin_Profile.objects.get(this_user = current_user)
    except Admin_Profile.DoesNotExist:
        raise Http404()

    my_hood =None
    try:
        my_hood = Neighbourhood.objects.get(admin = admin_profile)
    except Neighbourhood.DoesNotExist:
        raise Http404()

    if my_hood:
        longitude = my_hood.location[0]
        latitude = my_hood.location[1]
    

    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude,longitude],
                    popup='<h5>My neighbourhood.</h5>',
                    tooltip=f'{my_hood.hood_name}',
                    icon=folium.Icon(icon='glyphicon-home', color='blue')).add_to(m),
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=50,
        popup=f'{my_hood.hood_name}',
        color='#428bca',
        fill=True,
        fill_color='#428bca'
    ).add_to(m),

    map_page = m._repr_html_()    
      
    title = admin_profile.this_user.username
    return render(request, 'my-admin-profile.html', {"profile": admin_profile, "title": title, "hood": my_hood, "map_page":map_page})









  
    