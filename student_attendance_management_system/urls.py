from django.urls import path

from .views import (
    CourseListView,
    AttendanceView
)


urlpatterns = [

    path('courses/', CourseListView.as_view(), name='courses'),
    path('attendance/<str:course>/', AttendanceView.as_view(), name='attendance'),


]