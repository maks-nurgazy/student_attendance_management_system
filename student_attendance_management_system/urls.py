from django.urls import path

from .views import (
    CourseListView,
    TeachersCourseListView,
    AttendanceView,
    AttendanceDetailView,
)


urlpatterns = [

    path('courses/', CourseListView.as_view(), name='courses'),
    path('<int:teacher_id>/courses/', TeachersCourseListView.as_view(), name='teachers_courses'),
    path('<str:course>/attendance/', AttendanceView.as_view(), name='attendance'),
    path('<str:course>/attendance/<int:attendance_id>', AttendanceDetailView.as_view(), name='attendance_detail'),
]