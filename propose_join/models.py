from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta
from registration.models import Profile
from django.urls import reverse
from datetime import datetime
import datetime
from vote.models import VoteModel


class ProposedClub(VoteModel,models.Model):
    name=models.ForeignKey(User,on_delete=models.PROTECT)
    club_name=models.CharField(max_length=200,unique=True)
    club_info =models.TextField(max_length=20000)
    club_logo=models.ImageField(upload_to='media_/club_logo',)
    date = models.DateTimeField(default=timezone.now, blank=True)
    pollend=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return  str(self.club_name) + " by " + str(self.name)

    def get_url(self):
        return reverse('propose_join:detailview',kwargs={"pk":self.pk})



class ExistingClub(models.Model):
    club_name  = models.CharField(max_length=200,unique=True)
    admin = models.ManyToManyField(User,related_name="club_admins")
    club_info  =models.TextField(max_length=20000)
    club_logo = models.ImageField(upload_to='media_/club_logo', blank=True)
    club_members = models.ManyToManyField(User,related_name="club_members")

    def __str__(self):
        return str(self.club_name) + " admin--> " + str(self.admin)

    def get_url(self):
        return reverse('propose_join:detailview2', kwargs={"pk": self.pk})




# class ClubMember(models.Model):
#     user_name = models.OneToOneField(User,on_delete=models.PROTECT)
#     clubs_joined = models.ManyToManyField(ExistingClub)
#
#     def __str__(self):
#         return str(self.user_name)
