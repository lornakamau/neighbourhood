import folium
import random
import string
from django.shortcuts import render, redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Neighbourhood, Admin, Occupant, Business, Amenity, Post
from django.contrib.auth.decorators import login_required
from .email import send_signup_email_admin, send_signup_email_resident
from .forms import AdminProfileForm, NeighbourhoodForm, AddResidentForm, PostForm, BusinessForm, AmenityForm, ChangePasswordForm
from django.contrib.auth import authenticate
from django.contrib import messages

@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    admin= None
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        pass

    occupant = None
    try:
        occupant = Occupant.objects.get(user = current_user)
    except Occupant.DoesNotExist:
        pass

    if admin:
        return redirect(admin_profile)
    elif occupant:
        return redirect(user_profile)
    else:
        raise Http404    

@login_required(login_url='/accounts/login/')
def send_email(request):
    current_user = request.user
    email = current_user.email
    name = current_user.username
    send_signup_email_admin(name, email)
    return redirect(create_admin)


@login_required(login_url='/accounts/login/')
def create_admin(request):
    current_user = request.user
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect(create_hood)

    else:
        form = AdminProfileForm()
      
    title = "Admin profile "
    return render(request, 'create-admin.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def create_hood(request):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404()

    my_hood = None
    try:
        my_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        pass

    if my_hood:
        return redirect(admin_profile)

    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = admin
            hood.save()
        return redirect(admin_profile)

    else:
        form = NeighbourhoodForm()
      
    title = "Create Hood"
    return render(request, 'create-hood.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def admin_profile(request):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404()

    my_hood =None
    try:
        my_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        raise Http404()

    if my_hood:
        longitude = my_hood.location[0]
        latitude = my_hood.location[1]
    

    m = folium.Map(location=[latitude, longitude], zoom_start=16)
    folium.Marker([latitude,longitude],
                    popup='<h5>My neighbourhood.</h5>',
                    tooltip=f'{my_hood.name}',
                    icon=folium.Icon(icon='glyphicon-home', color='blue')).add_to(m),
    hospitals = Amenity.objects.filter(category='hospital', neighbourhood=my_hood)
    police_posts = Amenity.objects.filter(category='police', neighbourhood=my_hood)
    businesses = Business.objects.filter(neighbourhood=my_hood)
    schools = Amenity.objects.filter(category='school', neighbourhood=my_hood)
    for hospital in hospitals:
        hosp_longitude = hospital.location[0]
        hosp_latitude = hospital.location[1]
        folium.Marker([hosp_latitude,hosp_longitude],
                    popup=f'<p>{hospital.contact}</p>',
                    tooltip=f'{hospital.name}',
                    icon=folium.Icon(icon='glyphicon-plus-sign', color='purple')).add_to(m), 
    for post in police_posts:
        post_longitude = post.location[0]
        post_latitude = post.location[1]
        folium.Marker([post_latitude,post_longitude],
                    popup=f'<p>{post.contact}</p>',
                    tooltip=f'{post.name}',
                    icon=folium.Icon(icon='glyphicon-flag', color='darkgreen')).add_to(m), 
    for business in businesses:
        biz_longitude = business.location[0]
        biz_latitude = business.location[1]
        folium.Marker([biz_latitude,biz_longitude],
                    popup=f'<p>{business.name}</p>',
                    tooltip=f'{business.email}',
                    icon=folium.Icon(icon='glyphicon-shopping-cart', color='darkred')).add_to(m), 
    for school in schools:
        sch_longitude = school.location[0]
        sch_latitude = school.location[1]
        folium.Marker([sch_latitude,sch_longitude],
                    popup=f'<p>{school.contact}</p>',
                    tooltip=f'{school.name}',
                    icon=folium.Icon(icon='glyphicon glyphicon-pencil', color='darkblue')).add_to(m),

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=200,
        popup=f'{my_hood.name}',
        color='#428bca',
        fill=True,
        fill_color='#428bca'
    ).add_to(m),

    map_page = m._repr_html_() 

    posts = Post.objects.filter(neighbourhood=my_hood) 
      
    title = admin.user.username + " | MyNeighbourhood"
    return render(request, 'admin-profile.html', {"profile": admin, "title": title, "hood": my_hood, "map_page":map_page, "posts":posts})


@login_required(login_url='/accounts/login/')
def add_resident(request):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404()

    try:
        my_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        form = AddResidentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            this_resident =User.objects.create_user(username, email, password)
            occupant = Occupant(user=this_resident, neighbourhood=my_hood, name=name)
            occupant.save()
            
            my_hood.occupants = len(Occupant.objects.filter(neighbourhood = my_hood))+1
            my_hood.save()
            send_signup_email_resident(name, username, password,admin.user.username, my_hood.name, email)
            
        return redirect(admin_profile)

    else:
        form = AddResidentForm()
      
    title = "Add occupant"
    return render(request, 'add-occupant.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def update_hood(request):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404()
    
    try:
        my_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        pass

    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        if form.is_valid():
            my_hood.name = form.cleaned_data['name']
            my_hood.location = form.cleaned_data['location']
            my_hood.save()
        return redirect(admin_profile)

    else:
        form = NeighbourhoodForm()
      
    title = "Update Hood"
    return render(request, 'update-hood.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def delete_hood(request):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404()
    
    try:
        my_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        pass

    admin.delete()
    current_user.delete()

    return redirect(index)


@login_required(login_url='/accounts/login/')
def add_amenity(request):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404()
    
    try:
        my_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        pass    

    if request.method == 'POST':
        form = AmenityForm(request.POST)
        if form.is_valid():
            amenity = form.save(commit=False)
            amenity.neighbourhood = my_hood
            amenity.save()
        return redirect(admin_profile)

    else:
        form = AmenityForm()
      
    title = "Add Amenity"
    return render(request, 'add-amenity.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def user_profile(request):
    current_user = request.user
    try:
        occupant = Occupant.objects.get(user = current_user)
    except Occupant.DoesNotExist:
        raise Http404()

    my_hood = occupant.neighbourhood
    longitude = my_hood.location[0]
    latitude = my_hood.location[1]       

    m = folium.Map(location=[latitude, longitude], zoom_start=16)
    folium.Marker([latitude,longitude],
                    popup='<h5>My neighbourhood.</h5>',
                    tooltip=f'{my_hood.name}',
                    icon=folium.Icon(icon='glyphicon-home', color='blue')).add_to(m),
    hospitals = Amenity.objects.filter(category='hospital', neighbourhood=my_hood)
    police_posts = Amenity.objects.filter(category='police', neighbourhood=my_hood)
    businesses = Business.objects.filter(neighbourhood=my_hood)
    for hospital in hospitals:
        hosp_longitude = hospital.location[0]
        hosp_latitude = hospital.location[1]
        folium.Marker([hosp_latitude,hosp_longitude],
                    popup=f'<p>{hospital.contact}</p>',
                    tooltip=f'{hospital.name}',
                    icon=folium.Icon(icon='glyphicon-plus-sign', color='purple')).add_to(m), 
    for post in police_posts:
        post_longitude = post.location[0]
        post_latitude = post.location[1]
        folium.Marker([post_latitude,post_longitude],
                    popup=f'<p>{post.contact}</p>',
                    tooltip=f'{post.name}',
                    icon=folium.Icon(icon='glyphicon-flag', color='darkgreen')).add_to(m), 
    for business in businesses:
        biz_longitude = business.location[0]
        biz_latitude = business.location[1]
        folium.Marker([biz_latitude,biz_longitude],
                    popup=f'<p>{business.email}</p>',
                    tooltip=f'{business.name}',
                    icon=folium.Icon(icon='glyphicon-shopping-cart', color='darkred')).add_to(m), 

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=200,
        popup=f'{my_hood.name}',
        color='#428bca',
        fill=True,
        fill_color='#428bca'
    ).add_to(m),

    map_page = m._repr_html_()  

    posts = Post.objects.filter(neighbourhood=my_hood)
      
    title = occupant.name + " | MyNeighbourhood"
    return render(request, 'user-profile.html', {"profile": occupant, "title": title, "hood": my_hood, "map_page":map_page, "posts":posts})


@login_required(login_url='/accounts/login/')
def delete_resident_profile(request):
    current_user = request.user
    try:
        occupant = Occupant.objects.get(user = current_user)
    except Occupant.DoesNotExist:
        raise Http404()
    occupant.delete()
    current_user.delete()
    
    return redirect(index)


@login_required(login_url='/accounts/login/')
def change_password(request):
    current_user = request.user    

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_password']
            new_pass = form.cleaned_data['new_password']
            confirm_pass = form.cleaned_data['confirm_password']
            user = authenticate(username=current_user.username, password=old_pass)
            if user is not None:
                if new_pass == confirm_pass:
                    current_user.set_password(new_pass)
                    current_user.save()
                    messages.success(request, 'Your password was updated successfully!')
                    return redirect(user_profile)
                else:
                    messages.warning(request, 'Your passwords did not match.')
                
            else:
                messages.warning(request, 'Your old password is incorrect.')    

    else:
        form = ChangePasswordForm()
      
    title = "Change password"
    return render(request, 'change-password.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def change_profile_photo(request):
    current_user = request.user
    try:
        profile = Occupant.objects.get(user = current_user)
    except Occupant.DoesNotExist:
        raise Http404()
    
    if request.method == 'POST':
        profile.profile_pic = request.FILES['img']        
        profile.save()
        return redirect(user_profile)

    title = "Profile photo"    
    return render(request, 'update-prof-pic.html', {"title": title})


@login_required(login_url='/accounts/login/')
def add_business(request):
    current_user = request.user
    try:
        occupant = Occupant.objects.get(user = current_user)
    except Occupant.DoesNotExist:
        raise Http404()
    
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.neighbourhood = occupant.neighbourhood
            business.save()
        return redirect(user_profile)

    else:
        form = BusinessForm()
      
    title = "Add Business"
    return render(request, 'add-business.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def make_post(request):
    current_user = request.user
    admin = None
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        pass

    admin_hood =None
    try:
        admin_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        pass

    if admin:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.occupant = admin.user
                post.neighbourhood = admin_hood       
                post.save()
            return redirect(admin_profile)

        else:
            form = PostForm()

    occupant = None
    try:
        occupant = Occupant.objects.get(user = current_user)                
    except Occupant.DoesNotExist:
        pass 

    if occupant:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.occupant = occupant.user
                post.neighbourhood = occupant.neighbourhood         
                post.save()
            return redirect(user_profile)

        else:
            form = PostForm()
        
    title = "Add Post"
    return render(request, 'make-post.html', {"form": form, "title": title})


@login_required(login_url='/accounts/login/')
def residents_list(request):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404()
    
    try:
        my_hood = Neighbourhood.objects.get(admin = admin)
    except Neighbourhood.DoesNotExist:
        raise Http404()

    residents = Occupant.objects.filter(neighbourhood=my_hood)

    title = "Occupants"
    return render(request, 'occupants-list.html', {"title": title, "residents":residents, "hood":my_hood})


@login_required(login_url='/accounts/login/')
def delete_resident(request, res_id):
    current_user = request.user
    try:
        admin = Admin.objects.get(user = current_user)
    except Admin.DoesNotExist:
        raise Http404() 

    try:
        occupant = Occupant.objects.get(pk = res_id)
    except Occupant.DoesNotExist:
        raise Http404() 

    u_account=occupant.user
    occupant.delete()
    u_account.delete()   
    
    return redirect(residents_list)