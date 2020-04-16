from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    #test = models.CharField(max_length=50 , default='')
    #dob = models.DateField(blank=True,null=True)
    #conf_status = models.BooleanField(blank=True,default=False)
    gender_choices = (
        ('Male','Male'),
        ('Female','Female'),
        ('Neutral','Neutral'),
    )
    gender = models.CharField(max_length=10,choices=gender_choices,default='Neutral')
    Category_choices = (
        ('UG1','UG1'),
        ('UG2','UG2'),
        ('UG3','UG3'),
        ('UG4','UG4'),
        ('Phd','Phd'),
        ('PG','PG'),
    )
    ug = models.CharField(max_length=10,choices=Category_choices,default='UG1')
    image = models.ImageField(default="default.jpg", upload_to = 'profile_pics' )


    def __str__(self):
        return f'{self.user.username} Profile'
