from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import Signup_form, AddProfile ,EditPasswordFrom
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

def register(request):
    if request.method == 'POST':
        form = Signup_form(request.POST)
        form1 = AddProfile(request.POST, request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            m = form1.save(commit=False)
            m.user = user
            m.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('emailverify')
    else:
        form=Signup_form()
        form1 = AddProfile()

    context = {
        'form' : form,
        'form1': form1
    }
    return render(request,'registration/register1.html',context)

def emailverify(request):
    return render(request, 'registration/emailverify.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        messages.success(request, f'Account Created! Log In Now')
        return redirect('login')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def resetpassword(request):
    if request.method == 'POST':
        user_email=request.POST.get('user_email')
        user = User.objects.get(email=user_email)
        mails=User.objects.values_list('email',flat=True)
        if user_email in mails:
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('verifyemail')
    else:
        return render(request,'registration/enter-email.html')

def verifyemail(request):
    return render(request, 'registration/verifyemail.html')

def reset(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = EditPasswordFrom()
        return render(request,'registration/newpassword.html',{'form':form,'user':user.email})
        #user.save()
        # return redirect('home')
        #messages.success(request, f'Account backedup! Log In Now')
        #return redirect('login')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid')

def reset_password(request):
    if request.method == 'POST':
        user_email=request.POST.get('user_email')
        user=User.objects.get(email=user_email)
        pass1=request.POST['password']
        pass2=request.POST['confirm_password']
        if pass1 == pass2:
            user.set_password(pass1)
            user.save()
        else:
            form=EditPasswordFrom()
            messages.success(request, f"Password didn't match! Try again")
            return render(request,'registration/newpassword.html',{'user':user_email,'form':form})
        return redirect('login')
    else:
        return HttpResponse('Wrong way')
