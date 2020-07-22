# Generated by Django 3.0.8 on 2020-07-22 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('neighbourhoodApp', '0011_admin_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='name',
            field=models.CharField(default='Fullname', max_length=90),
        ),
        migrations.AlterField(
            model_name='amenity',
            name='category',
            field=models.CharField(choices=[('police', 'Police Post'), ('hospital', 'Healthcare center'), ('school', 'School')], max_length=50),
        ),
        migrations.AlterField(
            model_name='occupant',
            name='name',
            field=models.CharField(default='Fullname', max_length=90),
        ),
        migrations.AlterField(
            model_name='post',
            name='occupant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
