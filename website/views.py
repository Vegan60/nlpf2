from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from website.forms import UserForm,UserProfileInfoForm, AddNewTicketForm
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.urls import reverse
import datetime
#from django.views.generic import TemplateView
#from django.conf import settings
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request,'website/index.html')
@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'website/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'website/login.html', {})

def intranet(request):
    return render(request, 'intranet/home.html', locals())

@login_required
def user_create_ticket(request):
    if request.method == 'POST':
        ticket_form = AddNewTicketForm(data=request.POST)
        if ticket_form.is_valid():
            now = datetime.date.today()
            ticket = ticket_form.save(commit=False)
            ticket.tag = now.strftime('%Y-%m-%d %H:%M') +request.user.email
            ticket.client_mail = request.user.email
            print(ticket.tag)
            if 'image' in request.FILES:
                print('found it')
                ticket.image = request.FILES['image']
            ticket.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print(ticket_form.errors)
    else:
        ticket_form = AddNewTicketForm()
    context = {'ticket_form' : ticket_form}
    return render(request,'intranet/create_ticket.html',
                          {'ticket_form' : ticket_form})


def clients(request):
    return HttpResponse("Clients page")

def appointments(request):
    return HttpResponse("Appointments page")

