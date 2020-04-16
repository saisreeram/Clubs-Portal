from django.urls import reverse,resolve

class TestUrls:

#-----------------------------forum----------------------------------------

    def test_post_detail(self):
        path = reverse('post-detail',kwargs={'pk':1})
        assert resolve(path).view_name == 'post-detail'

    def user_home(self):
        path = reverse('user-home')
        assert resolve(path).view_name == 'user-home'

    def test_post_update(self):
        path = reverse('post-update',kwargs={'pk':1})
        assert resolve(path).view_name == 'post-update'

    def test_post_delete(self):
        path = reverse('post-delete',kwargs={'pk':1})
        assert resolve(path).view_name == 'post-delete'

#------------------------------------------------------------------------
