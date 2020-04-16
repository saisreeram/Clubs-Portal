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
from .models import Post, Comments, NotificationsPost, NotificationsEvents
from .forms import Add_Post,Add_Comment,Search_Post
from events.forms import AddEventForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from propose_join.models import ExistingClub
from django.db.models import Q
from events.models import Events
from django.template.loader import render_to_string
from itertools import chain
from operator import attrgetter

# Create your views here.
@login_required
def index(request):
    cuser = request.user
    PNoti = NotificationsPost.objects.filter(user = cuser).filter(read = False)
    ENoti = NotificationsEvents.objects.filter(user = cuser).filter(read = False)
    count = PNoti.count() + ENoti.count()
    club = ExistingClub.objects.get(club_name='Global')
    if request.method == 'POST':
        form = Add_Post(request.POST or None)
        form1 = Search_Post(request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            title = request.POST.get('title')
            form = Post.objects.create(title=title, author=request.user, content=content, in_club=club)
            form.save()
            messages.success(request, f'Posted')
            return redirect('user-home')
        if form1.is_valid() and (form.is_valid() == False):
            form=Add_Post()
            search_post = request.POST.get('search_post')
            posts = Post.objects.filter(in_club=ExistingClub.objects.get(club_name='Global')).filter(Q(title__icontains=search_post) | Q(content__icontains=search_post)).order_by('-date_posted')
            paginator = Paginator(posts,5)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            context = {
                'posts': posts,
                'form' : form,
                'form1':form1,
                'count':count,
            }
            return render(request,'forum/index.html', context)


        elif form1.is_valid() and form.is_valid():
            posts = Post.objects.filter(in_club=ExistingClub.objects.get(club_name='Global')).order_by('-date_posted')
            paginator = Paginator(posts,5)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            context = {
                'posts': posts,
                'form' : form,
                'form1':form1,
                'count':count,
            }
            return render(request,'forum/index.html', context)

    else:
        form=Add_Post()
        form1=Search_Post()

    posts = Post.objects.filter(in_club=ExistingClub.objects.get(club_name='Global')).order_by('-date_posted')
    paginator = Paginator(posts,5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'posts': posts,
        'form' : form,
        'form1':form1,
        'count':count,
    }
    return render(request,'forum/index.html', context)


def post_detail(request, pk):
    is_liked = False
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id):
        is_liked = True
    comments = Comments.objects.filter(comment_to=post).order_by('-date_posted')
    paginator = Paginator(comments,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    if request.method == 'POST':
        form = Add_Comment(request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            form = Comments.objects.create(comment_to=post, author=request.user, content=content)
            form.save()
            con = "Someone Commented on your Post"
            note = NotificationsPost.objects.create(postid = post,content = con,user = post.author,read = False)
            note.save()
            messages.success(request, f'Comment Posted')
            return redirect('post-detail', pk=pk)
    else:
        form=Add_Comment()
    context = {
        'post' : post,
        'comments' : comments,
        'form' : form,
        'total_likes': post.total_likes(),
        'is_liked': is_liked,
    }
    return render(request,'forum/post_detail.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def forum_of_club(request, club_id):
    object = ExistingClub.objects.get(pk = club_id)
    if request.method == 'POST':
        form = Add_Post(request.POST or None)
        form1 = Search_Post(request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            title = request.POST.get('title')
            in_club = get_object_or_404(ExistingClub, pk=club_id)
            form = Post.objects.create(title=title, author=request.user, content=content, in_club=in_club)
            form.save()
            messages.success(request, f'Posted')
            return redirect('club_forum' ,club_id=club_id)
        if form1.is_valid() and (form.is_valid() == False):
            form=Add_Post()
            search_post = request.POST.get('search_post')
            posts = Post.objects.filter(in_club=ExistingClub.objects.get(pk=club_id)).filter(Q(title__icontains=search_post) | Q(content__icontains=search_post)).order_by('-date_posted')
            paginator = Paginator(posts,5)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            in_club = [get_object_or_404(ExistingClub, pk=club_id)]
            context = {
                'posts': posts,
                'form' : form,
                'form1':form1,
                'inclub':in_club,
                'object':object,
            }
            return render(request,'forum/club_forum.html', context)


        elif form1.is_valid() and form.is_valid():
            posts = Post.objects.filter(in_club=ExistingClub.objects.get(pk=club_id)).order_by('-date_posted')
            paginator = Paginator(posts,5)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            in_club = [get_object_or_404(ExistingClub, pk=club_id)]
            context = {
                'posts': posts,
                'form' : form,
                'form1':form1,
                'inclub':in_club,
                'object':object,
            }
            return render(request,'forum/club_forum.html', context)

    else:
        form=Add_Post()
        form1=Search_Post()

    posts = Post.objects.filter(in_club=ExistingClub.objects.get(pk=club_id)).order_by('-date_posted')
    paginator = Paginator(posts,5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    in_club = [get_object_or_404(ExistingClub, pk=club_id)]
    context = {
        'posts': posts,
        'form' : form,
        'form1':form1,
        'inclub':in_club,
        'object':object,
    }
    return render(request,'forum/club_forum.html', context)

def posts_of_club(request, club_id, thread_id):
    pass

@login_required
def like_post(request):
    print(request.POST.get('id'))
    post = get_object_or_404(Post, pk=request.POST.get('id'))
    is_liked = True
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        con = "Someone Liked your Post"
        note = NotificationsPost.objects.create(postid = post,content = con,user = post.author,read = False)
        note.save()
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes':post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('forum/like_section.html',context,request=request)
        return JsonResponse({'form':html})


def event_of_club(request, club_id):
    if request.method == 'POST':
        form3 = AddEventForm(request.POST or None)
        if form3.is_valid():
            event_name = request.POST.get('event_name')
            about_event = request.POST.get('about_event')
            event_from = request.POST.get('event_from')
            event_to = request.POST.get('event_to')
            venue = request.POST.get('venue')
            in_club = get_object_or_404(ExistingClub, pk=club_id)
            form3 = Events.objects.create(event_name =event_name, about_event =about_event, event_from=event_from, event_to=event_to, venue=venue, in_club=in_club)
            form3.save()
            con = "An Event was announced in your club"
            for i in in_club.club_members.all():
                note = NotificationsEvents.objects.create(eventid = form3,content = con,user = i,read = False)
                note.save()
            messages.success(request, f'Event added successfully')
            return redirect('club_forum',club_id=club_id)
    else:
        form3=AddEventForm()
    context = {
        'form3':form3
    }
    return render(request,'events/post_event.html', context)


def notifications(request):
    cuser = request.user
    PNoti = NotificationsPost.objects.filter(user = cuser)
    ENoti = NotificationsEvents.objects.filter(user = cuser)
    Noti = sorted(
    chain(PNoti, ENoti),
    key=attrgetter('date_posted'),reverse=True)
    context = {
        'Noti': Noti,
    }
    PPNoti = NotificationsPost.objects.filter(user = cuser)
    EENoti = NotificationsEvents.objects.filter(user = cuser)
    for note in PPNoti:
        note.read = True
        note.save()
    for note in EENoti:
        note.read = True
        note.save()
    return render(request, 'forum/notifications.html', context)
