from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView
)

from events.forms import AddEventForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from propose_join.models import ExistingClub
from django.db.models import Q
from events.models import Events
from django.template.loader import render_to_string
from .models import Events


def list_event_of_club(request,club_id):
    events = Events.objects.filter(in_club=ExistingClub.objects.get(pk=club_id)).order_by('-event_from')

    context = {
        'events':events,
    }
    return render(request,'events/list_event.html', context)

def event_detail1(request,event_id):
    event = get_object_or_404(Events, pk=event_id)

    context = {
        'event':event,
    }
    return render(request,'events/event_about.html', context)

def list_event_of_user(request):
    clubs = ExistingClub.objects.filter(club_members=request.user)
    events = Events.objects.all().order_by('-event_from')

    context = {
        'events':events,
        'clubs':clubs,
    }
    return render(request,'events/list_event1.html', context)
