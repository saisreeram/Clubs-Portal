from django.db import models
from propose_join.models import ExistingClub

# Create your models here.
class Events(models.Model):
    event_name = models.CharField(max_length=100)
    about_event = models.TextField()
    event_from = models.DateTimeField()
    event_to = models.DateTimeField()
    in_club = models.ForeignKey(ExistingClub, on_delete=models.CASCADE)
    venue = models.TextField()

def get_absolute_url(self):
    return reverse('club_forum', kwargs={'club_id': self.pk})    
