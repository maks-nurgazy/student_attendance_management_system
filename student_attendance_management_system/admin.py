from django.contrib import admin

from .models import Course, Attendance, AttendanceReport


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'date')


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'student', 'status')
