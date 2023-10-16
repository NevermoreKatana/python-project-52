from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from django.test import Client


class StatusCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.status = Status.objects.create(name="Test Status")

    # Ваще хер его знает почему он не проходит емае LERN IT, IT NICE METHOD
    def test_index_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Status")

    def test_index_view_unauthenticated(self):
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 302)

    def test_create_status_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_status'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.filter(name='New Status').count(), 1)

    def test_create_status_view_unauthenticated(self):
        response = self.client.post(reverse('create_status'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)

    def test_update_status_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('update_status',
                                            args=[self.status.id]),
                                    {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.get(id=self.status.id).name, 'Updated Status')

    def test_update_status_view_unauthenticated(self):
        response = self.client.post(reverse('update_status',
                                            args=[self.status.id]),
                                    {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)

    def test_delete_status_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_status', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.filter(id=self.status.id).count(), 0)

    def test_delete_status_view_unauthenticated(self):
        response = self.client.post(reverse('delete_status', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
