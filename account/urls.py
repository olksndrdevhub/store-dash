"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.signin_view, name='signin_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('signout/', views.signout_view, name='signout_view'),
    path('', views.profile_view, name='profile_view'),

    # hx urls
    path('hx-update-userpic/', views.hx_update_userpic, name='hx_update_userpic'),
]
