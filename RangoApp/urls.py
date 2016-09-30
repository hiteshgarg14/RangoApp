"""RangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from Rango import views


urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^rango/', include('Rango.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$',views.MyRegistrationView.as_view(),name='registration_register'), #TODO
    url(r'^accounts/', include('registration.backends.simple.urls')),
]

"""
The django-registration-redux package provides a number of different registration backends,
depending on your needs. For example you may want a two-step process, where user is sent a
confirmation email, and a verification link. Here we will be using the simple one-step registration
process, where a user sets up their account by entering in a username, email, and password, and is
automatically logged in.
 """
