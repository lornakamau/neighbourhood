from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField, AddressAutoHiddenField

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 90, default="Fullname") 
    profile_pic = CloudinaryField('Profile Picture')

    def __str__(self):
        return self.user.username

class Neighbourhood(models.Model):
    name = models.CharField(max_length = 80)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    occupants = models.IntegerField(default=1)
    location = LocationField(map_attrs={"center": [36.82, -1.29], "marker_color": "blue"})
    address = AddressAutoHiddenField(blank=True)

    def __str__(self):
        return self.name 

class Occupant(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 90, default="Fullname")  
    profile_pic = CloudinaryField('Profile Picture')
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete= models.CASCADE)
    home = LocationField(map_attrs={"center": [36.82, -1.29], "marker_color": "blue"}, blank=True)

    def __str__(self):
        return self.user.username
        
class Business(models.Model):
    name = models.CharField(max_length = 80)
    definition = models.CharField(max_length = 300)
    email = models.EmailField() 
    location = LocationField(map_attrs={"center": [36.82, -1.29], "marker_color": "blue"})
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Businesses"

AMENITY_CHOICES = (
    ('police','Police Post'),
    ('hospital', 'Healthcare center'),  
    ('school','School'),  
)

class Amenity(models.Model):
    name = models.CharField(max_length = 80)
    category = models.CharField(max_length=50, choices=AMENITY_CHOICES)
    location = models.CharField(max_length = 300)
    contact = models.CharField(max_length = 100)
    location = LocationField(map_attrs={"center": [36.82, -1.29], "marker_color": "blue"})
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

class Post(models.Model):
    message = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True, null = True)
    occupant = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete= models.CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-post_date']


    