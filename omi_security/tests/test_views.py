from django.test import TestCase
#from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class LogInTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        user_login = self.client.login(username="testuser", password="secret")
        self.assertTrue(user_login)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="testuser", password="secret")
        response1 = self.client.get("/")
        self.assertEquals(response1.status_code, 200)
        self.client.logout()
        response2 = self.client.get("/")
        self.assertEquals(response2.status_code, 302)

    def test_about(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)






