from django.shortcuts import render, redirect
from django.http import HttpResponse
from propose_join.models import ExistingClub
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    clubs = ExistingClub.objects.all()
    context = {
        'clubs':clubs,
    }
    return render(request,'home/index.html',context)
