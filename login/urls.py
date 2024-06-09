from django.contrib import admin
from django.urls import path
from login import views as loginviews
from home import views as homeviews
# git -> changing to chenges
# linha adiocionada para mandar o arquivo para a área de changes no source control
urlpatterns = [
    path('', loginviews.login, name='login'),
    path('home/', homeviews.home, name='home'),
    #login é uma fução de response da view
]
