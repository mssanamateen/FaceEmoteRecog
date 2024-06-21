"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
#from mysite.facedetect.views import userh
from facedetect import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.hom,name="hom"),
    path('userhome/',views.userh,name="userh"),
    path("register", views.register_request, name="register"),
    path('login/', views.loginn, name='loginn'),
    path('usrh/',views.usrh,name="usrh"),
    path('logout/',views.logout,name="logout"),
    path('contact/',views.contactView, name='contact'),
    path('success/', views.successView, name='success'),
    path('sendq/',views.sendquery, name='contact'),
    path('success/', views.successView, name='success'),
    path('camera/',views.facerec,name='facerec'),
]
