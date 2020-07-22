from django.contrib import admin
from .models import Admin, Amenity, Business, Neighbourhood, Post, Occupant

admin.site.register(Admin)
admin.site.register(Amenity)
admin.site.register(Business)
admin.site.register(Neighbourhood)
admin.site.register(Post)
admin.site.register(Occupant)