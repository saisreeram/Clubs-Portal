from django.contrib.auth.models import User
from registration.models import Profile
from notifications.models import Notification
import unittest

class Test_user(unittest.TestCase):
    def test_back(self):
        user=User.objects.create(first_name='narendra',last_name='reddy',email='ynarendrareddy186@gmail.com',
                                    username='ase',password='ase12345')
        user = User.objects.get(username='ase')
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        value=first_name+last_name+email
        self.assertEquals('narendra'+'reddy'+'ynarendrareddy186@gmail.com',value)

    def test_notification(self):
        noti=Notification.objects.create(username='ase3',sender='ase4',notifications='hi',date='11-02-2015 21:54:02')
        user = Notification.objects.get(username='ase3')
        sender = user.sender
        notif = user.notifications
        value=sender+notif
        self.assertEquals('ase4'+'hi',value)

    def test_profile(self):
        user=User.objects.create(first_name='narendra',last_name='reddy',email='ynarendrareddy186@gmail.com',
                                    username='ase2',password='ase12345')
        real_user=User.objects.get(username='ase2')
        user_p=Profile.objects.create(user=real_user,gender='Male',ug='UG1',image='default.png')
        user = Profile.objects.get(user=real_user)
        gender = user.gender
        category = user.ug
        value=gender+category
        self.assertEquals('Male'+'UG1',value)
