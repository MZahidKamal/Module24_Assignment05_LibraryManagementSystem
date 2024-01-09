from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    road_and_house = models.CharField(max_length=500)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username

"""
In Django models, fields are required by default. This means if you have a field in your model, Django will automatically
enforce that this field must be provided or it will raise an error. Unless you have not explicitly set blank=True or null=True.
"""
