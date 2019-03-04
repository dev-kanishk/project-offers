from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.PROTECT)

    phone_number = models.CharField( max_length=12,blank=False,default="") # validators should be a list

    def __str__(self):
        return self.user.username
