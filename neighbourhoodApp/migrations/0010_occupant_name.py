# Generated by Django 3.0.8 on 2020-07-20 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhoodApp', '0009_admin_amenity_business_neighbourhood_occupant_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='occupant',
            name='name',
            field=models.CharField(default='fullname', max_length=90),
        ),
    ]