import json
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, URLPatternsTestCase

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class UserTest(APITestCase, URLPatternsTestCase):
    """ Test module for User """

    urlpatterns = [
        path('api/auth/', include('users.urls')),
    ]

    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admin',
        )

        self.teacher = User.objects.create_user(
            email='teacher@test.com',
            password='teacher',
        )

        self.student1 = User.objects.create_user(
            email='student@test.com',
            password='student',
        )

    def test_login(self):
        """ Test if a user can login and get a JWT response token """
        url = reverse('login')
        data = {
            'email': 'admin@test.com',
            'password': 'admin'
        }
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['success'], True)
        self.assertTrue('access' in response_data)

    def test_student_registration(self):
        """ Test if a student can register """
        #              'first_name',
        #             'last_name',
        #             'email',
        #             'password',
        #             'role'

        url = reverse('register')
        data = {
            'first_name': 'testStudent2',
            'last_name': 'studentTest2',
            'email': 'student2@test.com',
            'password': 'student',
            'role': 3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_registration(self):
        """ Test if a teacher can register """
        #              'first_name',
        #             'last_name',
        #             'email',
        #             'password',
        #             'role'

        url = reverse('register')
        data = {
            'first_name': 'testTeacher2',
            'last_name': 'teacherTest2',
            'email': 'teacher2@test.com',
            'password': 'teacher',
            'role': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_all_users_as_admin(self):
        """ Test fetching all users. Restricted to admins """
        # Setup the token
        url = reverse('login')
        data = {'email': 'admin@test.com', 'password': 'admin'}
        response = self.client.post(url, data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        # Test the endpoint
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get(reverse('users'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), len(response_data['users']))

    def test_access_denied_all_students(self):
        """ Test fetching all users. Restricted to admins """
        # Setup the token
        url = reverse('login')
        data = {'email': 'student@test.com', 'password': 'student'}
        response = self.client.post(url, data)
        login_response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in login_response_data)
        token = login_response_data['access']

        # Test the endpoint
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = client.get(reverse('users'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response_data['success'])

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = 'test'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDONappdev.com'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123  ')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
