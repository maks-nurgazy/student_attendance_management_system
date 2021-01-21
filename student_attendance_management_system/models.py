from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from datetime import datetime

from student_attendance_management_system.managers import CustomUserManager


def current_time():
    return datetime.now()


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    TEACHER = 2
    STUDENT = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Course(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(User)
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='courses')


class Attendance(models.Model):
    date = models.DateTimeField(default=current_time)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')


class AttendanceReport(models.Model):
    attendance_\
        = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
