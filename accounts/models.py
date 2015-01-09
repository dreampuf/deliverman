from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.
class UserManager(auth_models.UserManager):
    #model = User
    pass

class User(auth_models.AbstractUser):
    objects = UserManager()

    country = models.CharField(null=True, max_length=85)
    department = models.CharField(null=True, max_length=30)
    gid = models.IntegerField(null=True)
    uid = models.IntegerField(null=True)
    photo = models.ImageField(null=True, upload_to="photos")
#
#
