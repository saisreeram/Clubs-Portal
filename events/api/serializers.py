from rest_framework.serializers import ModelSerializer,SerializerMethodField

from events.models import Events

class EventListSerializer(ModelSerializer):
    in_club = SerializerMethodField(read_only=True)

    def get_in_club(self, obj):
        # obj is model instance
        return obj.in_club.club_name
    class Meta:
        model = Events
        fields = [
            'in_club',
            # 'event_name',
            # 'about_event',
            'event_from',
            'event_to',
            'venue',
        ]

class EventDetailSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = [
            'event_name',
            'about_event',
            'event_from',
            'event_to',
            'in_club',
            'venue',
        ]
