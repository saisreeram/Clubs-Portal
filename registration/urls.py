from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    #path("login",views.login,name='login_url'),
    path("register",views.register,name ='signup_url'),
    #path("otp-verification",views.verify,name='otp_url'),
    #path("logout",views.logout,name='logout_url'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset, name='reset'),

]
