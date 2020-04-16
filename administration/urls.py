from django.urls import path ,include,path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('result1', views.result1, name='result1'),

]
