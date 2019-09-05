from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save

from .utlis import unique_slug_generator
# Create your models here.


# class User(AbstractUser):
#     is_verifieduser = models.BooleanField('user status', default=False)







class UserProfileInfo(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)

	phone_number = models.CharField( max_length=12,blank=False) # validators should be a list
	is_verifieduser = models.BooleanField(default=True)
	is_shopkeeper = models.BooleanField(default=False)
	is_user = models.BooleanField(default=True)

	def __str__(self):
		return self.user.username


class Categories(models.Model):
	filters = models.CharField(max_length=20)

	def __str__(self):
		return self.filters



class ShopProfile(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)

	shop_name = models.CharField(max_length=100,blank=False,unique=True)
	address = models.TextField(max_length=100)
	tag_line = models.TextField(max_length=40, blank = True)
	shop_discription = models.TextField(max_length=250)
	photo1 = models.ImageField(upload_to='images/',blank=False)
	photo2 = models.ImageField(upload_to='images/', blank=True)
	photo3 = models.ImageField(upload_to='images/', blank=True)
	photo4 = models.ImageField(upload_to='images/', blank=True)
	slug = models.SlugField(unique=True, blank=True)
	def __str__(self):
		return self.shop_name




class Offer_discription(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
	shop_name = models.CharField(max_length=100)
	text = models.TextField()
	offer_tag = models.CharField(max_length =100 , default="initial")
	index_photo = models.ImageField(upload_to='images/', default="/media/off2.jpg")

	categories = models.ForeignKey(Categories,related_name='offers',on_delete=models.CASCADE)
	address = models.TextField(max_length=100)
	ready_post = models.BooleanField(default=True)
	likes = models.ManyToManyField(User, blank=True, related_name='post_likes', default=0)
	slug = models.SlugField(unique=True, blank=True)
	comments = models.IntegerField(default=0)



	def __str__(self):
		return self.text

	def get_like_url(self):
		return reverse("interface:like-toggle", kwargs={"slug": self.slug})

	def get_api_like_url(self):
		return reverse("interface:like-api-toggle", kwargs={"slug": self.slug})

	def get_absolute_url(self):
		return reverse("index")



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



class Comments(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
	comment = models.TextField()
	offer_id = models.IntegerField()


class offer_images(models.Model):
	offer = models.ForeignKey(Offer_discription, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to='images/', blank=True)


pre_save.connect(pre_save_post_receiver, sender=Offer_discription)