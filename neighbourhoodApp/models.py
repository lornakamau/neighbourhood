from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Neighbourhood(models.Model):
    name = models.CharField(max_length = 80)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    occupants = models.ManyToManyField(Occupant, related_name="occupant")

    def __str__(self):
        return self.name

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

class Occupant(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    email = models.EmailField()
    profile_pic = CloudinaryField('Profile Picture')

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete() 

class Business(models.Model):
    name = models.CharField(max_length = 80)
    category = models.CharField(max_length = 30)
    location = models.CharField(max_length = 300)

    def __str__(self):
        return self.name





    