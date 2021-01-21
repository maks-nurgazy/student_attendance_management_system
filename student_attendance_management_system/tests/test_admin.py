from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='admin'
        )
        self.client.force_login(self.admin_user)
        self.student = get_user_model().objects.create_user(
            email="student@test.com",
            password="student",
            name='Test user full name'
        )
