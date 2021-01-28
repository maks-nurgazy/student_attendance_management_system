from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import (
    GenericAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Course, Attendance
from .serializers import (
    AdminCourseSerializer,
    TeacherCourseSerializer,
    StudentCourseSerializer,
    AttendanceSerializer,
    AttendancePostSerializer,
    CourseDetailSerializer
)

User = get_user_model()


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
            serializer = self.get_serializer_class()
            data = request.data
            if request.content_type != 'application/json':
                response = {
                    'success': False,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'Content type must be application/json'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializer = serializer(data=data)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                status_code = status.HTTP_200_OK
                course = serializer.save()
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Course added successfully'
                }
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_404_NOT_FOUND
                response = {
                    'success': False,
                    'statusCode': status_code,
                    'message': 'Error while serializing'
                }
                return Response(response, status=status_code)
        else:
            status_code = status.HTTP_403_FORBIDDEN
            response = {
                'success': False,
                'statusCode': status_code,
                'message': 'Access denied'
            }
            return Response(response, status=status_code)

    def get_serializer_class(self):
        user = self.request.user
        if user.role == 1:
            return AdminCourseSerializer
        elif user.role == 2:
            return TeacherCourseSerializer
        elif user.role == 3:
            return StudentCourseSerializer


class CourseDetailView(RetrieveUpdateDestroyAPIView, APIException):
    queryset = User.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        filter_kwargs = self.kwargs['id']
        try:
            obj = Course.objects.get(id=filter_kwargs)
        except ObjectDoesNotExist:
            raise APIException('Course not exists')
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class TeachersCourseListView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherCourseSerializer

    def get(self, request, teacher_id):
        teachers_courses = Course.objects.all().filter(teacher=teacher_id)
        serializer = self.get_serializer_class()
        serializer = serializer(teachers_courses, many=True)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched courses',
            'courses': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class AttendanceView(GenericAPIView):

    # permission_classes = [IsAuthenticated | TeacherOnly]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action',
            }
            return Response(response, status.HTTP_403_FORBIDDEN)

        if user.role == 2 or user.role == 1:
            course_in_url = kwargs['course']
            course = Course.objects.get(name=course_in_url)
            attendances = course.attendances
            serializer = self.get_serializer_class()
            serializer = serializer(attendances, many=True)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Attendances fetched successfully',
                'attendance': serializer.data
            }
            return Response(response, status=status_code)
        else:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action',
            }
            return Response(response, status.HTTP_403_FORBIDDEN)

    def post(self, request, course):
        user = request.user
        if user.role == 1 or user.role == 2:
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                status_code = status.HTTP_200_OK
                serializer.save()
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Attendance saved successfully'
                }
                return Response(response, status=status_code)
        else:
            status_code = status.HTTP_200_OK
            response = {
                'success': False,
                'statusCode': status_code,
                'message': 'You must be an admin user'
            }
            return Response(response, status=status_code)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AttendanceSerializer

        elif self.request.method == "POST":
            return AttendancePostSerializer


class AttendanceDetailView(GenericAPIView):
    serializer_class = AttendancePostSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == 1 or user.role == 2:
            attendance_id = kwargs['attendance_id']
            attendance = Attendance.objects.get(id=attendance_id)
            serializer = self.serializer_class(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        if user.role == 1 or user.role == 2:
            attendance_id = kwargs['attendance_id']
            attendance = Attendance.objects.get(id=attendance_id)
            serializer = self.serializer_class(attendance, data=request.data)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_200_OK
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Attendance updated successfully'
                }
                return Response(response, status=status_code)

    def delete(self, request, *args, **kwargs):
        attendance_id = kwargs['attendance_id']
        attendance = Attendance.objects.get(id=attendance_id)
        attendance.delete()
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'Attendance deleted successfully'
        }
        return Response(response, status=status_code)
