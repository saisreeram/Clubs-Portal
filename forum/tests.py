from django.test import TestCase

class testing_user():
    def 

    def test_call_view_loads(self):
        self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('forum:user-home')
        self.assertEquals(response.status_code, 200)
# Create your tests here.
