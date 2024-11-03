from django.contrib import admin
from django.urls import path
from login import views as loginviews
from home import views as homeviews

urlpatterns = [
    path('', loginviews.login, name='login'),
    path('logout_option', loginviews.logout_option, name='logout'),
    path('home/', homeviews.home, name='home'),
]
