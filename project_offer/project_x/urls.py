"""project_x URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from interface import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name="adi"),
    path("",views.Index.as_view(), name="index"),
    path("interface/",include("interface.urls")),
    path("shop/",views.shop, name="shop"),
    path("logout/",views.user_logout, name="logout"),
    path("special", views.special,name="special"),
    path("<int:pk>/", views.OfferDetailView.as_view(), name=" OfferDetailView"),
    path("categories/<int:pk>",views.Filters.as_view(), name="Filters"),
    path("upload_offer/",views.Upload_Offer, name="upload_offer"),
    path('viewoffer/',views.viewoffer, name="viewoffer"),
    url(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),
    url(r"edit/(?P<pk>\d+)/$",views.EditPost.as_view(),name="edit"),

    url(r'^', include('django.contrib.auth.urls')),
    path('shop_registration/',views.shop_registration,name='shopregistration'),
    path("<slug:slug>/",views.Shop_profile,name="shopprofile"),
    path("basic_app/user_login/",views.user_login),
    path("<int:pk>/comment/",views.comments, name="comments"),
    path("<int:pk>/delete_comment/",views.delete_comment, name="comment_delete"),
    path("<int:pk>/like/",views.like, name="like"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)