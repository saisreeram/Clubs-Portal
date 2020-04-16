"""clubsportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from home import views as home_views
from registration import views as register_views
from django.conf import settings
from django.conf.urls.static import static
from userprofile import views as profile_views
from forum import views as forum_views
from events import views as events_views
from propose_join import views as clubs_views
from forum import views as forum_views
from django.conf.urls import url
from notifications import views as notify_views
from administration import views as admin_views

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('administration/', admin_views.index, name="admin_page"),
    path('',home_views.index, name='home'),
    path('propose_join/',include("propose_join.urls")),
    path('registration/',include("registration.urls")),
    path('userprofile/',include("userprofile.urls")),
    path('home/', include("forum.urls")),
    path('administration/', include("administration.urls")),
    path('home/clubs', clubs_views.existingClubList, name='exlist'),
    path('home/proposed-clubs', clubs_views.proposedClubList, name='prlist'),
    path('home/joined-clubs', clubs_views.joinedClubList, name='jdlist'),
    path('home/joined-clubs/<int:club_id>/', forum_views.forum_of_club, name='club_forum'),
    path('home/joined-clubs/<int:club_id>/add-event/', forum_views.event_of_club, name='club_event'),
    path('home/joined-clubs/<int:club_id>/list_events/', events_views.list_event_of_club, name='list_club_event'),
    path('home/joined-clubs/list_events/', events_views.list_event_of_user, name='list_user_event'),
    path('home/joined-clubs/<int:event_id>/about', events_views.event_detail1, name='event_detail1'),
    path('home/joined-clubs/<int:club_id>/<int:thread_id>/', forum_views.posts_of_club, name='club_forum_posts'),
    path('home/propose-club', clubs_views.proposeClub, name='prclub'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/',register_views.register, name = 'register'),
    path('home/profile/',profile_views.profile, name = 'profile'),
    path('api/events/',include("events.api.urls")),
    path('api-token-auth/', obtain_jwt_token),
    path("home/profile/change_password",profile_views.change_password, name="change_password"),
    path('emailverify/',register_views.emailverify, name = 'emailverify'),
    path('resetpassword/',register_views.resetpassword,name = 'resetpassword'),
    path('verifyemail/',register_views.verifyemail, name = 'verifyemail'),
    path('reset_password/',register_views.reset_password, name = 'reset_password'),
    path("send",notify_views.send,name='send'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""
curl -X POST -d "username=rahul_admin&password=test1234" http://localhost:8000/api-token-auth/
curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMiwidXNlcm5hbWUiOiJyYWh1bF9hZG1pbiIsImV4cCI6MTU0NDU2Njc4NywiZW1haWwiOiIifQ.2GoWR9hSMATuh7oVk8f7LzPlxhDn78_mmvr0Tj1A5Hc" http://127.0.0.1:8000/api/events/

"""
