import unittest
from registration.views import login,register,emailverify,verifyemail
from notifications.views import notifications,send
from userprofile.views import profile,change_password
from django.urls import reverse,resolve
from django.contrib.auth.views import LoginView,LogoutView


class Test_urls(unittest.TestCase):

    def test_signup_redirect(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEquals(resolve(url).func,register)

    def test_login_redirect(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class,LoginView)

    def test_logout_redirect(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class,LogoutView)

    def test_notification_redirect(self):
        url = reverse('notifications')
        self.assertEquals(resolve(url).func,notifications)

    def test_send_redirect(self):
        url = reverse('send')
        self.assertEquals(resolve(url).func,send)

    def test_profile_redirect(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func,profile)

    def test_changepassword_redirect(self):
        url = reverse('change_password')
        self.assertEquals(resolve(url).func,change_password)

    def test_emailverify_redirect(self):
        url = reverse('emailverify')
        self.assertEquals(resolve(url).func,emailverify)

    def test_verifyemail_redirect(self):
        url = reverse('verifyemail')
        self.assertEquals(resolve(url).func,verifyemail)
