from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Donor'),
        (3, 'Buyer'),
    )
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)

class Donor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    # Add any other fields specific to donors

class Buyer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    # Add any other fields specific to buyers




class Category(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    

class Pet(models.Model):
    image = models.ImageField(upload_to='pets/', null=True, blank=True)
    description = models.TextField()
    breed = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    weight = models.FloatField()
    medical_conditions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.breed} - {self.age} years old"

