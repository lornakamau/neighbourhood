from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.home,name = 'home'),
    url(r'^email/$',views.email,name = 'email'),
    url(r'^create-profile-admin/$',views.create_profile_admin,name = 'create-profile-admin'),
    url(r'^create-hood/$',views.create_hood,name = 'create-hood'),
    url(r'^update-hood/$',views.update_hood,name = 'update-hood'),
    url(r'^my-admin-profile/$',views.my_admin_profile,name = 'my-admin-profile'),
    url(r'^add-resident/$',views.add_resident,name = 'add-resident'),
]