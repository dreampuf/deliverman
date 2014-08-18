from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
    )

# Create your models here.

#class User(AbstractUser):
#    country = models.CharField(max_length=85)
#    department = models.CharField(max_length=30)
#    groupid = models.IntegerField()
#    photo = models.ImageField(upload_to="photos")
#
#class UserManager(BaseUserManager):
#    model = User
#
