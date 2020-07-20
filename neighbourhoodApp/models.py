from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField, AddressAutoHiddenField

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Occupant(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = CloudinaryField('Profile Picture')

    def __str__(self):
        return self.user.username

class Neighbourhood(models.Model):
    name = models.CharField(max_length = 80)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    occupants = models.ManyToManyField(Occupant, related_name="occupant")
    location = LocationField(map_attrs={"center": [36.82, -1.29], "marker_color": "blue"})
    address = AddressAutoHiddenField(blank=True)

    def __str__(self):
        return self.name 

class Business(models.Model):
    name = models.CharField(max_length = 80)
    category = models.CharField(max_length = 30)
    location = models.CharField(max_length = 300)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Businesses"

class Amenity(models.Model):
    name = models.CharField(max_length = 80)
    category = models.CharField(max_length = 30)
    location = models.CharField(max_length = 300)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

class Post(models.Model):
    message = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True, null = True)
    occupant = models.ForeignKey(Occupant, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete= models.CASCADE)

    def __str__(self):
        return self.message



    