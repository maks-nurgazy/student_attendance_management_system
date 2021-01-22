from rest_framework import serializers

from users.models import User
from .models import Course, Attendance, AttendanceReport


class CourseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
        )


class AdminCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    course_students = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = Course
        fields = (
            'name',
            'teacher',
            'course_students',
            'students'
        )
        extra_kwargs = {
            'students': {'write_only': True},
        }

    def get_course_students(self, obj):
        query_set = obj.students
        return CourseUserSerializer(query_set, many=True).data


class TeacherCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, read_only=True)
    course_students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'name',
            'course_students'
        )

    def get_course_students(self, obj):
        query_set = obj.students
        return CourseUserSerializer(query_set, many=True).data


class StudentCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, read_only=True)

    class Meta:
        model = Course
        fields = (
            'name',
        )


class AttendanceSerializer(serializers.ModelSerializer):
    report = serializers.PrimaryKeyRelatedField(queryset=AttendanceReport.objects.all())

    class Meta:
        model = Attendance
        fields = ('date', 'course', 'report')
