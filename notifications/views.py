from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect# Create your views here.
@login_required(login_url="{% url 'login' %}")
def notifications(request):
    current_user = request.user
    username=str(current_user)
    notif=Notification.objects.filter(username=username)
    return render(request, 'notifications/view_notify.html',{'notification':notif})

@login_required(login_url="{% url 'login' %}")
def send(request):
    if request.method == 'POST':
        notf=request.POST.get('notf')
        users=request.POST.getlist('selected_users')
        list=[]
        for user in users:
            list.append(User.objects.get(username=user).email)
        mail = EmailMessage('Notification', notf , to=list)
        mail.send()

        current_user=request.user
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sender=str(current_user)
        for name in users:
            new=Notification.objects.create(username=name,sender=sender,notifications=notf,date=str(now))
            new.save()
        messages.success(request, f'Notification sent successfully')
        return redirect('notifications')
    else:
        users=User.objects.all()
        context={
            'users':users
        }
        return render(request,'notifications/send.html',context)
