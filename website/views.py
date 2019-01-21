from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from website.forms import UserForm,UserProfileInfoForm, AddNewTicketForm
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.urls import reverse
from website.models import UserProfileInfo, Ticket
#from django.views.generic import TemplateView
#from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.models import User

from .models import Ticket
import logging
import datetime
import django_tables2 as tables


logger = logging.getLogger(__name__)

def index(request):
    return render(request,'website/index.html')
def list_accepted(request):
    accepted_tickets = Ticket.objects.filter(tag='Accepted')
    return render(request, 'list_accepted.html', {'accepted': accepted_tickets})
def list_waiting(request):
    waiting_tickets = Ticket.objects.filter(tag='Waiting')
    return render(request, 'list_waiting.html', {'waiting': waiting_tickets})
def list_denied(request):
    denied_tickets = Ticket.objects.filter(tag='Denied')
    return render(request, 'list_denied.html', {'denied': waiting_tickets})
def answer(request, id):
    ticket = Ticket.objects.get(id=id)
    return render(request, 'answer.html', {'ticket': ticket})
def update_accept(request, id):
    logger.debug(request)
    waiting_tickets = Ticket.objects.filter(tag='Waiting')
    return redirect(request, '/website/intranet', {'waiting': waiting_tickets})
def update_denie(request, id):
    logger.debug(request)
    waiting_tickets = Ticket.objects.filter(tag='Waiting')
    return redirect(request, '/website/intranet', {'waiting': waiting_tickets})  
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
                if (username == 'bob') :
                    return redirect('/website/intranet')
                else :
                    return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'website/login.html', {})

@login_required
def intranet(request):
    return render(request, 'intranet/home.html', locals())

@login_required
def user_create_ticket(request):
    if request.method == 'POST':
        ticket_form = AddNewTicketForm(data=request.POST)
        if ticket_form.is_valid():
            now = datetime.datetime.now()
            ticket = ticket_form.save(commit=False)
            ticket.tag = str(now) + " - " + request.user.email
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

@login_required
def appointments(request):
    return HttpResponse("Appointments page")

@login_required
def clientblock(request):
    username_b = request.POST.get('username')
    user_c = User.objects.get(username=username_b)
    user_c.is_active = False
    user_c.save(update_fields=['is_active'])
    return redirect('/website/intranet/clients')

@login_required
def ticketaccept(request):
    ticket_tag = request.POST.get('tag')
    ticket_ = Ticket.objects.get(id=ticket_tag)
    ticket_.status = 'Accepted'
    ticket_.save(update_fields=['status'])
    return redirect('/website/intranet/appointments')

@login_required
def clientunblock(request):
    username_b = request.POST.get('username')
    user_c = User.objects.get(username=username_b)
    user_c.is_active = True
    user_c.save(update_fields=['is_active'])
    return redirect('/website/intranet/clients')


class ClientListView(generic.ListView):
    model = User
    context_object_name = 'clients'
    template_name = 'intranet/clients.html'

class TicketListView(generic.ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = 'intranet/tickets.html'

