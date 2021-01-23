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


class AttendanceReportSerializer(serializers.ModelSerializer):
    report_id = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceReport
        fields = (
            'report_id',
            'student',
            'status',
        )

    def get_report_id(self, obj):
        return obj.id

    def get_student(self, obj):
        query_set = obj.student
        return CourseUserSerializer(query_set).data

    def get_status(self, obj):
        if obj.status:
            return "Present"
        else:
            return "Absent"


class AttendanceSerializer(serializers.ModelSerializer):
    reports = AttendanceReportSerializer(many=True)
    course = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = (
            'date',
            'course',
            'reports'
        )

    # def get_attendance_report(self, obj):
    #     query_set = obj.reports
    #     return AttendanceReportSerializer(query_set, many=True).data

    def get_course(self, obj):
        return obj.course.name


class AttendancePostSerializer(serializers.ModelSerializer):
    course = serializers.CharField(max_length=30)
    reports = AttendanceReportSerializer(many=True)

    class Meta:
        model = Attendance
        fields = (
            'date',
            'course',
            'reports'
        )
