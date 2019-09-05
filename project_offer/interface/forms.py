from django import forms
from django.contrib.auth.models import User
from interface.models import UserProfileInfo, Offer_discription, ShopProfile,Comments, offer_images
from django.forms import formset_factory

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('phone_number','is_shopkeeper')

class Offer_discriptionForm(forms.ModelForm):
	class Meta():
		model = Offer_discription
		fields=('text','categories','index_photo','offer_tag')


class ShopProfileForm(forms.ModelForm):
    class Meta():
        model = ShopProfile
        fields=('shop_name','shop_discription','photo1','photo2','photo3','photo4','address')

class Comments_Form(forms.ModelForm):
    class Meta():
        model = Comments
        fields = ('comment',)

class offer_image_form(forms.ModelForm):
    class Meta():
        model = offer_images
        fields = ('photo',)

Offer_imageFormset = formset_factory(offer_image_form, extra=10)