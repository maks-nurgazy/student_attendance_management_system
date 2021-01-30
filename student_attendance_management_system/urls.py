from django.urls import path

from .views import (
    CourseListView,
    CourseDetailView,
    TeacherListView,
    TeacherDetailView,
    TeachersCourseListView,
    StudentListView,
    StudentDetailView,
    StudentsCourseListView,
    AttendanceView,
    AttendanceDetailView,
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('teachers/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/<int:teacher_id>/courses/', TeachersCourseListView.as_view(), name='teachers_courses'),
    path('students/', StudentListView.as_view(), name='students'),
    path('students/<int:student_id>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:student_id>/courses/', StudentsCourseListView.as_view(), name='teachers_courses'),
    path('<str:course_name>/attendance/', AttendanceView.as_view(), name='attendance'),
    path('<str:course_name>/attendance/<int:attendance_id>', AttendanceDetailView.as_view(), name='attendance_detail'),
]
