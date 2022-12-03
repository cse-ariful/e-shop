from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    class Type(models.TextChoices):
        USER = "1", "USER"
        STAFF = "2", "STAFF"
        ADMIN = "3", "ADMIN"
    email = models.CharField(blank=False,null=False,unique=True,max_length=250)
    first_name = models.CharField(max_length=100,blank=False,null=False)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    is_mobile_verified = models.BooleanField(default=False, blank=False)
    is_email_verified = models.BooleanField(default=False, blank=False)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.USER)
    profile_picture = models.ImageField(upload_to="media/profile_pictures", blank=True, null=True)
