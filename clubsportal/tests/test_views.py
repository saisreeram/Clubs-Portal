from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from forum.views import post_detail
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestViews:
    def test_post_detail_authenticated(self):
        mixer.blend('posts.Post')
        path = reverse('post-detail',kwargs={'pk':1})
        request = RequestFactory().get(path)
        request.user = mixer.blend('User')

        response = product_detail(request,pk=1)
        assert response.status_code == 200
