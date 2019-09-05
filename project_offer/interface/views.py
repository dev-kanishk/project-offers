from django.shortcuts import render
from interface.forms import (UserForm, UserProfileInfoForm, Offer_discriptionForm, ShopProfileForm,
                            Comments_Form, Offer_imageFormset)
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView,RedirectView)
from django.views import View
import requests
from django.shortcuts import render, redirect
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from . import models
from .models import UserProfileInfo
from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from braces.views import SelectRelatedMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from django.contrib import messages
from django.http import JsonResponse
import json
from django.utils.safestring import mark_safe
# from django_user_agents.utils import get_user_agent
User = get_user_model()
# Create your views here.
class Index(ListView):
    # context_object_name = "filter"
    # model = models.Categories
    context_object_name = 'offer_details'
    model = models.Offer_discription
    template_name = "index.html"

@login_required
def user_logout(request):
    logout(request)
    return render(request,"login.html",{})



def special(request):
       return render(request,"special.html",{})


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''



            if result['success']:

                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
            #
            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']
                profile.save()
                login(request,user)

                registered = True
                if request.POST['is_shopkeeper'] == "on":
                    return HttpResponseRedirect(reverse('shopregistration'))

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'register.html',
               {'user_form':user_form,
                  'profile_form':profile_form,
                  'registered':registered,})



def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("someone tried to login and failed")
            return HttpResponse("username and password combination not valid")

    else:
         return render(request,'login.html',{})

class Filters(DetailView):
    context_object_name = "filter"
    model = models.Categories
    template_name = "categories.html"


# class OfferDetailView(DetailView):
#     context_object_name = 'offer_details'
#     model = models.Offer_discription
#     template_name = 'offer_detail.html'

class OfferDetailView(View):

    def get(self, request, *args, **kwargs):
        offer = get_object_or_404(models.Offer_discription, pk=kwargs['pk'])
        list_offer =models.Offer_discription.objects.all()
        comment_s = models.Comments.objects.filter(offer_id=kwargs['pk'])
        comment_count = comment_s.count()
        offer_like = models.Offer_discription.objects.filter(pk=kwargs['pk'])[0].likes.all()

        if request.user in offer_like:
            liked = True
        else:
            liked = False

        comment_list = []
        x = int(comment_count)
        while x > (comment_count - 3):
            if x ==  0:
                break
            print(comment_s[x-1])
            comment_list.append(comment_s[x-1])


            x -= 1

        comment_list.reverse()



        context = {'offer':offer,'list_offer':list_offer,'comment_s':comment_s,'liked':liked,'comment_s_3':comment_list}
        return render(request, 'offer_detail.html', context)

@login_required
def like(request,pk):
    offer = models.Offer_discription.objects.filter(pk = pk)[0].likes.all()
    print(offer)

    if request.user in offer:
            models.Offer_discription.objects.filter(pk = pk)[0].likes.remove(request.user)
            offer = models.Offer_discription.objects.filter(pk = pk)[0].likes.all()
            count = str(offer.count())
            print(offer.count)
            data ={
            'action':0,
            'count':count
            }
            data = json.dumps(data)

            return JsonResponse(mark_safe(data), safe=False)

            return HttpResponse(offer.count())
    else:
            models.Offer_discription.objects.filter(pk = pk)[0].likes.add(request.user)
            offer = models.Offer_discription.objects.filter(pk = pk)[0].likes.all()
            count = str(offer.count())
            print(offer.count)
            data ={
            'action':1,
            'count':count
            }
            data = json.dumps(data)

            return JsonResponse(mark_safe(data), safe=False)
            return HttpResponse(offer.count())
def comments(request,pk):

    if request.method == 'POST':
        form = Comments_Form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user=request.user
            instance.offer_id = pk
            instance.save()
            instance = form.save()
            comment_pk = instance.pk
            print(request.POST['comment'])
            comment = str(request.POST['comment'])
            data = {
            'comment':comment,
            'done':True,
            'user':request.user.username,
            'pk' : comment_pk
            }

            data = json.dumps(data)
            print(data)

            return JsonResponse(mark_safe(data), safe=False)
            # return HttpResponseRedirect("/"+str(pk)+"/")
            # return json.dumps(data)
            return HttpResponse("done")

def delete_comment(request,pk):

    instance = models.Comments.objects.filter(pk=pk)

    print(instance)
    offer_pk = instance[0].offer_id
    instance.delete()
    data = {

            'done':True,

            }

    data = json.dumps(data)
    return JsonResponse(mark_safe(data), safe=False)
    return HttpResponseRedirect("/"+str(offer_pk)+"/")






def Upload_Offer(request):
    if not request.user.is_authenticated:
        return HttpResponse("LOGIN FIRST")
    # verify= UserProfileInfo.objects.raw(is_varifieduser)
    # if not verify:
    #     return HttpResponse("Your registration is still not verified")
    if request.method == 'POST':
        form = Offer_discriptionForm(request.POST, request.FILES)
        formset = Offer_imageFormset(request.POST or None, request.FILES or None)
        print(formset)

        if form.is_valid() and formset.is_valid():
            # form.photo = request.FILES['images']
            print('voko')
            instance = form.save(commit=False)
            instance.user=request.user
            shop_namegot=models.ShopProfile.objects.filter(user=request.user).values('shop_name')


            instance.shop_name=shop_namegot[0]["shop_name"]
            shop_addressgot=models.ShopProfile.objects.filter(user=request.user).values('address')

            instance.address=shop_addressgot[0]['address']
            instance.save()
            for f in formset:

                    photo = f.cleaned_data.get('photo')
                    if photo:
                        models.offer_images(offer=instance,photo=photo).save()





            return HttpResponseRedirect(reverse('index'))
        return HttpResponse("form not valid ")
    else:
           form = Offer_discriptionForm()
           formset = Offer_imageFormset()
           return render(request,'upload_offer.html',{'form': form, 'formset':formset})



# @login_required(login_url="/interface/user_login/")
def viewoffer(request):
    user = request.user

    template ='viewoffer.html'


        # Do other stuff...
    user_posts = models.Offer_discription.objects.filter(user=request.user)

    return render(request, template, {'user_posts':user_posts,'user':user})


class EditPost(LoginRequiredMixin, UpdateView):
    model = models.Offer_discription
    form_class = Offer_discriptionForm
    template_name = 'edit_offer.html'






    # def test_func():
    #     obj = self.get_object()
    #     if obj.user == self.request.user:
    #         return True
    #     else:
    #         return False
    def dispatch(self, request,*args,**kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return Http404("Your are not allowed to edit this post")
        return super(EditPost, self).dispatch(request,*args,**kwargs)



class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Offer_discription
    select_related = ("user",)
    success_url = reverse_lazy("index")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)






def shop_registration(request):
    if not request.user.is_authenticated:
        return HttpResponse("LOGIN FIRST")
    if request.method == 'POST':
        form = ShopProfileForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit="false")
            first_name = instance.shop_name.split()[0]
            instance.slug = first_name+"_"+request.user.username
            instance.user=request.user
            instance.save()
            form.save()
            return HttpResponse("registered cool")
        else:
            return HttpResponse("form not valid")
    form = ShopProfileForm()
    return render(request,'shop_registration.html',{'form':form})


def Shop_profile(request,slug):

    obj=models.ShopProfile.objects.filter(slug=slug)
    offers = models.Offer_discription.objects.filter(shop_name = obj[0].shop_name)


    context={'shop':obj[0],'offers':offers}
    template_name = 'shop.html'
    return render(request,template_name,context)


def shop(request):
    template_name="shop.html"
    return render(request,template_name,{})