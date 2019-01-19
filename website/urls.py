from django.conf.urls import url
from django.urls import path

from website import views
# SET THE NAMESPACE!
app_name = 'website'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('intranet', views.intranet, name='intranet'),
    path('intranet/clients', views.clients, name='clients'),
    path('intranet/appointments', views.appointments, name='appointments'),
]