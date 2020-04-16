from django.db import models

# Create your models here.
class Notification(models.Model):
    username = models.CharField(max_length=100 ,default='')
    sender = models.CharField(max_length=100,default='')
    notifications = models.CharField(max_length=1000,null=True)
    date = models.CharField(max_length=50,default='')

    def __str__(self):
        return self.username
