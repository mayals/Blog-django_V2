from django.urls import path
from .import views 

from django.conf.urls.static import static
from django.conf import settings


app_name='users'

urlpatterns = [
    path('register/', views.registeruser, name='register'),
    path('login/', views.loginuser, name ='login'),
    path('logout/', views.logoutuser, name ='logout'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('myprofile_update/',views.myprofile_update,name='myprofile-update'),
]