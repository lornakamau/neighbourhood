from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

class Neighbourhood(models.Model):
    name = models.CharField(max_length = 80)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    occupants = models.ManyToManyField(Profile, related_name="occupant")

    def __str__(self):
        return self.name

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()