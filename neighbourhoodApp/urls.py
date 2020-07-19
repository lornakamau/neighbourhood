from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.home,name = 'home'),
    url(r'^email/$',views.email,name = 'email'),
     url(r'^create_profile_admin/$',views.create_profile_admin,name='create_profile_admin'),
]