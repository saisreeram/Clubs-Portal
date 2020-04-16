from rest_framework.generics import ListAPIView ,RetrieveAPIView

from rest_framework.filters import SearchFilter,OrderingFilter

from events.models import Events
from .serializers import EventListSerializer,EventDetailSerializer

class EventDetailAPIView(RetrieveAPIView):
    queryset = Events.objects.all()
    serializer_class = EventDetailSerializer

class EventListAPIView(ListAPIView):
    # queryset = Events.objects.all()
    serializer_class = EventListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['in_club__club_name','venue','event_from','event_to']
    ordering_fields = ('event_from','in_club__club_name')

    def get_queryset(self,*args,**kwargs):
        queryset_List = Events.objects.all()
        return queryset_List
