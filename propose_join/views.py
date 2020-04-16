from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ExistingClub,ProposedClub
from administration.models import Onpollclub
from .forms import ProposedClubForm
from django.contrib.auth import get_user_model
from registration.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import UserManager
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.urls import reverse
import datetime, time
from django.utils import timezone
import data as data


def existingClubList(request):
    mem = request.user
    clubs = ExistingClub.objects.exclude(club_name='Global')
   # clubs = clubs1.exclude(club_members=mem)
    paginator = Paginator(clubs,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'clubs': clubs,
    }
    return render(request,'propose_join/exlist.html', context)

def proposedClubList(request):
    voter=request.user
    totalstudent=Profile.objects.all().count()
    clubs = Onpollclub.objects.all()
    for i in clubs:
        start=i.date
        milistart=int(time.mktime(start.timetuple())) * 1000
        #print(milistart)
        #print('nf')
        currtime=timezone.now()
        milicurr=(int(time.mktime(currtime.timetuple())) * 1000) + 330*60*1000
        #print(milicurr)
        endtime=int(milistart) + 7*24*60*60*1000
        timeleft=int(endtime - milicurr)
        #print(timeleft)
        i.pollend=timeleft
        i.save()
        for a in clubs:
            if a.pollend<0:
                vote=a.num_vote_up
            #   print(vote)
                threshhold=(vote/totalstudent)*100
                if threshhold >10:
                    instance=ExistingClub.objects.create(club_name=a.club_name, club_info=a.club_info,club_logo=a.club_logo)
                    instance.admin.add(a.name)
                    instance.club_members.add(a.name)
                a.delete()

    clubs = Onpollclub.objects.all()
    paginator = Paginator(clubs,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'clubs': clubs,
    }
    return render(request,'propose_join/prlist.html', context)



def joinedClubList(request):
    clubs = ExistingClub.objects.filter(club_members=request.user).exclude(club_name='Global')
    paginator = Paginator(clubs,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'clubs': clubs,
    }
    return render(request,'propose_join/jdlist.html', context)


def proposeClub(request):
    form = ProposedClubForm(request.POST, request.FILES)
    if request.method == 'POST':
        form = ProposedClubForm(request.POST, request.FILES)
        #print(request.user)
        #print(request.POST)
        if form.is_valid():
            club1 = form.save(commit=False)
            club1.name = request.user
            #CustomUser.objects.get(Username=request.user)
            club1.save()
            messages.success(request, f'Your Club Has Been Proposed')
            return redirect('user-home')
    else:
        form = ProposedClubForm()
    context = {
            'form' : form,
    }
    return render(request, 'propose_join/home.html', context)


@login_required
def add_to_join(request):
    if request.method == "POST":
        clubname=request.POST.get('club-joined')
     #   print(request.user)
        cuser = request.user
        existingclub = ExistingClub.objects.get(club_name = clubname)
        existingclub.club_members.add(cuser)
        return redirect('exlist')

    else:

        return redirect('user-home')

"""@login_required
def list(request):
    voter=request.user
    totalstudent=Profile.objects.all().count()
    qs = Onpollclub.objects.all()
    for i in qs:
        start=i.date
        milistart=int(time.mktime(start.timetuple())) * 1000
        #print(milistart)
        #print('nf')
        currtime=timezone.now()
        milicurr=(int(time.mktime(currtime.timetuple())) * 1000) + 330*60*1000
        #print(milicurr)
        endtime=int(milistart) + 7*24*60*60*1000
        timeleft=int(endtime - milicurr)
        #print(timeleft)
        i.pollend=timeleft
        i.save()

    for i in qs:

        if i.pollend<0:
            vote=i.num_vote_up
         #   print(vote)

            threshhold=(vote/totalstudent)*100
            if threshhold >10:
                for a in qs:
                    instance=ExistingClub.objects.create(club_name=a.club_name, club_info=a.club_info,club_logo=a.club_logo)
                    instance.admin.add(a.name)


            i.delete()

    qs = Onpollclub.objects.all()





    return render(request, "propose_join/list.html", {"qs": qs})
"""

def voting(request):
    if request.method == "POST":
        club_id =request.POST.get('club-id')
        #print("upvote",club_id)

        cuser=request.user
        user=User.objects.get(username=cuser)
        club1 = Onpollclub.objects.get(pk=club_id)
        action = request.POST.get('vote')
        if action == 'yes':

            club1.votes.up(user.id)
            return redirect(reverse('propose_join:detailview', kwargs={"pk": club_id}))

        elif action == 'no':
            club1.votes.down(user.id)
            return redirect(reverse('propose_join:detailview', kwargs={"pk": club_id}))


        return  redirect (reverse('propose_join:detailview', kwargs={"pk":club_id}))

    else:
        return redirect("user-home")


# def votedown(request):
#     if request.method == "POST":
#         club_id = request.POST.get('club-id')
#         cuser = request.user
#         print("downvote",club_id)
#         user = User.objects.get(username=cuser)
#         club1 = ProposedClub.objects.get(pk=club_id)
#         club1.votes.down(user.id)
#
#         return redirect(reverse('propose_join:detailview', kwargs={"pk": club_id}))
#     else:
#         return redirect("home:index")


class ProposedClubDetailView(DetailView):
    template_name = 'propose_join/proposedclub_detail.html'

    model = Onpollclub
    def get_object(self, queryset=None,*args,**kwargs):
        pk=self.kwargs['pk']
        instance = Onpollclub.objects.get(pk=pk)
        start = instance.date
        milistart = int(time.mktime(start.timetuple())) * 1000
        currtime = timezone.now()
        milicurr = (int(time.mktime(currtime.timetuple())) * 1000) + 330 * 60 * 1000
        endtime = int(milistart) + 7 * 24 * 60 * 60 * 1000
        timeleft = int(endtime - milicurr)
        instance.pollend=timeleft
        end=instance.pollend
        if end < 0:
            #vote = instance.num_vote_up
            #totalstudent = Profile.objects.all().count()
            #threshhold = (vote / totalstudent) * 100
            #if threshhold > 10:
                #insta = ExistingClub.objects.create(club_name=instance.club_name, club_info=instance.club_info,club_logo=instance.club_logo)
                #insta.admin.add(instance.name)
            instance.delete()
            return Onpollclub.DoesNotExist("object doesnt exist")

        else:
            return instance

    def get_context_data(self, **kwargs):
        context = super(ProposedClubDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        instance = Onpollclub.objects.get(pk=pk)
        d = instance.date
        for_js = int(time.mktime(d.timetuple())) * 1000

        #if time.now()
        context['for_js'] = for_js


        return context

    # def update_counter(request):
    #     if request.method == 'POST':
    #         player = Player.objects.get()
    #         player.blur_quantity = request.POST['counter']
    #         player.save()
    #         message = 'update successful'
    #     return HttpResponse(message)

class JoinedClubDetailView(DetailView):
    template_name = 'propose_join/joinedclub_detail.html'

    model = ExistingClub
    def get_object(self, queryset=None,*args,**kwargs):
        pk=self.kwargs['pk']
        try:
            instance = ExistingClub.objects.get(pk=pk)
            return instance

        except:
            return ExistingClub.DoesNotExist("object doesnt exist")

def quitclub(request,pk):

     if request.method == "POST":
            club_id =request.POST.get('club-id')
            cuser=request.user
            user=User.objects.get(username=cuser)
            club1=ExistingClub.objects.get(pk=club_id)
            action = request.POST.get('quit')
            if action == 'quit':

                club1.club_members.remove(user)
                return redirect('jdlist')


def ListCLubMembers(request,pk):
    club = ExistingClub.objects.get(pk=pk)
    if request.method == "POST":
            user_id = request.POST.get('usr')
            print(user_id)
            user = User.objects.get(username = user_id)
            action = request.POST.get('quit')
            if action == 'quit':
                club.club_members.remove(user)
                return redirect('propose_join:listmem', pk = club.id)
    context = {
        'club': club,
    }
    return render(request,'propose_join/club_members.html', context)
