# -*- coding: cp1252 -*-
from django.conf.urls import url,include
from interface import views
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.urls import path
app_name='interface'

urlpatterns=[
   url(r'^register/$',views.register, name="register"),
   url(r'^user_login/$',views.user_login, name="user_login"),
   url(r'^login/$', LoginView.as_view(template_name='login.html')),
   url(r'^logout/$', LogoutView.as_view(template_name='accounts/logout.html')),
   url(r'^reset-password/$', PasswordResetView.as_view (from_email='reset_password')),
   path('reset-password/done/', PasswordResetDoneView.as_view (template_name='reset_password_done')),
   url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   url(r'^', include('django.contrib.auth.urls')),

]
