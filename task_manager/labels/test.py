from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from task_manager.labels.models import Labels


class LabelsCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.label = Labels.objects.create(name="Test Label")

    def test_labels_view_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_labels_view_unauthenticated(self):
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 302)

    def test_labels_create_view_unauthenticated(self):
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, 302)

    def test_labels_delete_view_unauthenticated(self):
        response = self.client.get(reverse('labels_delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)

    def test_labels_update_view_unauthenticated(self):
        response = self.client.get(reverse('labels_update', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('labels_delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Labels.objects.filter(id=self.label.id).count(), 1)

    def test_labels_update_view_post_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('labels_update', args=[self.label.id]), {'name': 'Updated Label'})
        self.assertEqual(response.status_code, 302)
        updated_label = Labels.objects.get(id=self.label.id)
        self.assertEqual(updated_label.name, 'Updated Label')
