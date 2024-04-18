from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from testapp.manager import UserManager
# Create your models here.

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active =models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    
    objects = UserManager()
    
    def __str__(self):
        return  self.email
