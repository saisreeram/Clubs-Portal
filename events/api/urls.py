from django.urls import path
from . import views
from .views import (
    EventListAPIView,
    EventDetailAPIView
)
urlpatterns = [
    path('', EventListAPIView.as_view(),name='events_api'),
    path('<pk>', EventDetailAPIView.as_view(),name='events_detail'),
]
