from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course
from .serializers import AdminCourseSerializer, TeacherCourseSerializer, StudentCourseSerializer, AttendanceSerializer


class CourseListView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role == 1:
            courses = Course.objects.all()
            serializer = self.get_serializer_class()
            serializer = serializer(courses, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched courses',
                'courses': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        elif user.role == 2:
            teachers_courses = Course.objects.all().filter(teacher=user.id)
            serializer = self.get_serializer_class()
            serializer = serializer(teachers_courses, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched courses',
                'courses': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        elif user.role == 3:
            student_courses = Course.objects.filter(students=user.id)
            serializer = self.get_serializer_class()
            serializer = serializer(student_courses, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched courses',
                'courses': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if user.role == 1:
            serializer = self.serializer_class(data=request.data)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                status_code = status.HTTP_200_OK
                data = serializer.validated_data
                course = Course.objects.create(**data)
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Course added successfully'
                }

                return Response(response, status=status_code)
        else:
            return None

    def get_serializer_class(self):
        user = self.request.user
        if user.role == 1:
            return AdminCourseSerializer
        elif user.role == 2:
            return TeacherCourseSerializer
        elif user.role == 3:
            return StudentCourseSerializer


class AttendanceView(GenericAPIView):
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.role == 2:
            serializer = self.serializer_class(data=request.data)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Attendance saved successfully',
                }
                return Response(response, status=status_code)

        else:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
