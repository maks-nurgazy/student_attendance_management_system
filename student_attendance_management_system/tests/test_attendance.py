import json

from django.contrib.auth import get_user_model
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient

User = get_user_model()


class AttendanceTest(APITestCase, URLPatternsTestCase):
    """ Test module for Attendance """

    urlpatterns = [
        path('api/auth/', include('users.urls')),
        path('api/', include('student_attendance_management_system.urls')),
    ]

    def setUp(self):
        # Creating a ADMIN user
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admin',
        )

        # Registering TEACHER
        register_url = reverse('register')
        data = {
            'first_name': 'testTeacher',
            'last_name': 'teacherTest',
            'email': 'teacher@test.com',
            'password': 'teacher',
            'role': 2
        }
        response = self.client.post(register_url, data)
        response_data = json.loads(response.content)
        self.teacher = response_data['user']

        # Registering STUDENT
        data = {
            'first_name': 'testStudent',
            'last_name': 'studentTest',
            'email': 'student@test.com',
            'password': 'student',
            'role': 3
        }

        response = self.client.post(register_url, data)
        response_data = json.loads(response.content)
        self.student = response_data['user']

        # Request body SETTINGS (GET AND SET TOKEN)
        login_url = reverse('login')
        data = {'email': 'teacher@test.com', 'password': 'teacher'}
        response = self.client.post(login_url, data)
        login_response_data = json.loads(response.content)
        token = login_response_data['access']
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_course_add_as_admin(self):
        pass

    def test_get_attendance(self):
        pass
        # response = self.client.get(reverse('attendance', kwargs={'course': 'math'}))
        # response_data = json.loads(response.content)
        # print(response_data)
