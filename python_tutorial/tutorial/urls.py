from django.urls import path
from . import views

app_name = 'tutorial'

urlpatterns=[
    path('home/',views.home,name="home"),
    path('gettoken/',views.gettoken,name='gettoken'),
    path('mail/',views.mail,name='mail'),
]



