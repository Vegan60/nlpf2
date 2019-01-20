from django.conf.urls import url
from . import views

# urlpatterns = [
#    url(r'^$', views.post_list, name='post_list'),

from django.urls import path

from website import views
# SET THE NAMESPACE!
app_name = 'website'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('intranet/', views.intranet, name='intranet'),
    path('intranet/clients', views.ClientListView.as_view(), name='clients'),
    path('intranet/clientblock', views.clientblock, name='clientblock'),
    path('intranet/clientunblock', views.clientunblock, name='clientunblock'),
    path('intranet/appointments', views.appointments, name='appointments'),
]