from django import forms
from django.forms import ModelForm
from website.models import UserProfileInfo
from website.models import Ticket
from django.contrib.auth.models import User

class UserForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  class Meta():
    model = User
    fields = ('username','password','email')

class UserProfileInfoForm(ModelForm):
  class Meta():
    model = UserProfileInfo
    fields = ('portfolio_site','profile_pic')

class AddNewTicketForm(ModelForm):
  class Meta():
    model = Ticket
    fields = ('address', 'country', 'direction', 'image')


