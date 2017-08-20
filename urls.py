"""mysite URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

import oauth2client.contrib.django_util.site as django_util_site


urlpatterns = [
    url(r'^fusionmaps/', include('fusionmaps.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^oauth2/', include(django_util_site.urls)),
    url(r'^oauth2callback', 'fusionmaps.views.auth_return'),
    url(
        r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'}
    ),
    # url(r'^login/$', 'django.contrib.auth.views.login', name="my_login")
]
