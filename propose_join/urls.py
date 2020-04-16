from django.urls import path
from . import views

app_name= "propose_join"    
urlpatterns=[
   # path('button', views.proposeClub, name='button'),
   # path('list', views.list, name='list'),
    path('home/proposed-clubs/add', views.voting, name='voting'),
    #path('detailview/remove', views.votedown, name='votedown'),
    #path('existing',views.existingclub,name='existing'),
    #path('existing/count', views.passed, name='passed'),
    path('existing/add', views.add_to_join, name='add_to_join'),
    #path('myclub', views.joined, name='myclub'),
    path('detailview/<int:pk>/', views.ProposedClubDetailView.as_view(), name='detailview'),
    path('detailview2/<int:pk>/', views.JoinedClubDetailView.as_view(), name='detailview2'),
    path('detailview2/<int:pk>/rem',views.quitclub,name='quitclub'),
    path('clubmembers/<int:pk>/', views.ListCLubMembers, name="listmem"),



]
