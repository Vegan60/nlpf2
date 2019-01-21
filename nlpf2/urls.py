"""nlpf2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from website import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list_accepted', views.list_accepted, name='list_accepted'),
    path('list_denied', views.list_denied, name='list_denied'),
    path('list_waiting', views.list_waiting, name='list_waiting'),
    url(r'^answer/(?P<id>[0-9]+)$', views.answer, name='answer'),
    url(r'^update/accept/(?P<id>[0-9]+)$', views.update_accept, name='accept'),
    url(r'^update/denie/(?P<id>[0-9]+)$', views.update_denie, name='denie'),
    url(r'^$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^website/',include('website.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
]
