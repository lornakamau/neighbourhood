# Generated by Django 3.0.8 on 2020-07-20 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhoodApp', '0007_amenity_business_neighbourhood_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amenity',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='business',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='neighbourhood',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='neighbourhood',
            name='occupants',
        ),
        migrations.RemoveField(
            model_name='occupant',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='post',
            name='occupant',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Amenity',
        ),
        migrations.DeleteModel(
            name='Business',
        ),
        migrations.DeleteModel(
            name='Neighbourhood',
        ),
        migrations.DeleteModel(
            name='Occupant',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
