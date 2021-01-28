from django.db import models
from django.utils import timezone

from users.models import User


def current_time():
    return timezone.now()


def get_status_in_string(status):
    if status:
        return "Present"
    else:
        return "Absent"


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    students = models.ManyToManyField(User, blank=True, related_name='student_courses')
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='teacher_courses', null=True,
                                blank=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    date = models.DateTimeField(default=current_time)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')

    def __str__(self):
        return f'{self.course.name} {self.date.date()}'


class AttendanceReport(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='reports')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} {get_status_in_string(self.status)}'
