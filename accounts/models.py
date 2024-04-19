from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length= 50)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=50)
    def __str__(self):
        return str(self.user.email)