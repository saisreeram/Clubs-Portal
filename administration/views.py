from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from propose_join.models import ExistingClub,ProposedClub
from propose_join.forms import ProposedClubForm
from django.contrib.auth import get_user_model
from .models import Onpollclub
from django.contrib.auth.models import User
from registration.models import  Profile
from datetime import datetime
from django.utils import timezone

from dateutil.relativedelta import relativedelta

def index(request):
    clubs = ProposedClub.objects.all()
    return render(request,'administration/admin.html',{"clubs":clubs})

def result(request):
    ab = ProposedClub.objects.all()
    cs=None
    for a in ab:
        if a.club_name == request.POST['name']:
            cs = a.name
            a.delete()
            break;

    mail=User.objects.get(username=cs).email
    fullname1 = request.POST['message']
    send_mail(
        'Your club is rejected',
        fullname1,
        'iiits2021@gmail.com',
        [mail],
        fail_silently=False,
    )
    clubs = ProposedClub.objects.all()
    return render(request, 'administration/admin.html', {"clubs":clubs})

# Create your views here.
def result1(request):
    ab = ProposedClub.objects.all()
    cs=None
    for a in ab:
        if a.club_name == request.POST['name']:
            print(a)
            Onpollclub.objects.create(club_name=a.club_name,name=a.name,club_info=a.club_info,club_logo=a.club_logo)
            cs = a.name
            a.delete()
            break;
    mail = User.objects.get(username=cs).email
    send_mail(
        'Your club is accepted',
        'Hii,              Tell all your friends to participate in polls                                 thanks ',
        'iiits2021@gmail.com',
        [mail],
        fail_silently=False,
    )
    clubs = ProposedClub.objects.all()
    return render(request, 'administration/admin.html', {"clubs":clubs})
