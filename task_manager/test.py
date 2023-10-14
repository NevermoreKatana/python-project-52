from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

class UserCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_create_user(self):
        response = self.client.post('/users/create/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)

        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_update_user(self):
        response = self.client.post(f'/users/{self.user.id}/update/', {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'User')
        self.assertEqual(updated_user.username, 'updateduser')

    def test_delete_user(self):
        response = self.client.post(f'/users/{self.user.id}/delete/')
        self.assertEqual(response.status_code, 302)

        self.assertEqual(User.objects.filter(username='testuser').count(), 0)