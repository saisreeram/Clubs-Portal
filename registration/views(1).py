from django.shortcuts import render
from django.http import HttpResponse
from .forms import Signup_form , Add_profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as new,authenticate,logout as exit
from django.core.mail import EmailMessage
import random

#otp=random.randint(100000,999999)

# Create your views here.
def register(request):
    if request.method == 'POST':
        form=Signup_form(request.POST)
        form1=Add_profile(request.POST)
        if form.is_valid() and form1.is_valid():
            user1=form.save()
            user1.set_password(user1.password)
            form2 = form1.save(commit=False)
            form2.user=user1
            form2.save()
            user_mail=request.POST.get('email')
            #mail = EmailMessage('E-mail verification', str(otp) , to=[user_mail])#,fail_silently=True)
            #mail.send()
            return render(request,'registration/email-confirmation.html')
            return HttpResponse('Signed up')
    else:
        form=Signup_form()
        form1=Add_profile()
    return render(request,'registration/register.html',{'form_inst':form,'form1':form1})

def login(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            new(request,user)
            return HttpResponse('Logged in')
    else:
        form=AuthenticationForm()
    return render(request,'registration/login.html',{'form_inst':form})

def logout(request):
    if request.method=='POST':
        exit(request)
        return HttpResponse('Logged out successfully')

def verify(request):
    if request.method=='POST':
        otp1=request.POST.get('typed_otp')
        if otp1 == str(otp):
            return HttpResponse('correct otp')
        else:
            return HttpResponse('wrong otp')
    else:
        return HttpResponse('wrong way')
