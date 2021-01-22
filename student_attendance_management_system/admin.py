from django.contrib import admin


from .models import Course, Attendance, AttendanceReport





@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    pass
