from rest_framework import serializers

from users.models import User
from .models import Course, Attendance, AttendanceReport


class CourseStudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return User.objects.create_student(**validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password'
        )

    def validate(self, data):
        email = data.get("email", None)
        ModelClass = self.Meta.model
        id = data.get("id", None)

        if not id and ModelClass.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        return data


class AdminCourseSerializer(serializers.ModelSerializer):
    course_id = serializers.SerializerMethodField('get_course_id')
    students = CourseStudentSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        student_list = validated_data.pop('students', None)
        teacher_id = validated_data.pop('teacher', None)
        if (student_list is not None) and (teacher_id is not None):
            course = Course.objects.create(**validated_data, teacher=teacher_id)
            self.add_subject_student(student_list=student_list, course=course)
        elif (student_list is None) and (teacher_id is not None):
            course = Course.objects.create(**validated_data, teacher=teacher_id)
        elif (student_list is not None) and (teacher_id is None):
            course = Course.objects.create(**validated_data)
            self.add_subject_student(student_list=student_list, course=course)
        else:
            course = Course.objects.create(**validated_data)
        return Course.objects.get(id=course.id)

    def add_subject_student(self, student_list, course):
        for student_obj in student_list:
            try:
                student_id = student_obj['id']
                course.students.add(student_id)
            except KeyError:
                serializer = CourseStudentSerializer(data=student_obj)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    student_email = serializer.save()
                    course.students.add(student_email)

    class Meta:
        model = Course
        fields = (
            'course_id',
            'name',
            'teacher',
            'students'
        )

    def get_course_id(self, obj):
        return obj.id


class TeacherCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, read_only=True)
    course_students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'course_students'
        )

    def get_course_students(self, obj):
        query_set = obj.students
        return CourseStudentSerializer(query_set, many=True).data


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
        return CourseStudentSerializer(query_set).data

    def get_status(self, obj):
        if obj.status:
            return "Present"
        else:
            return "Absent"


class AttendanceSerializer(serializers.ModelSerializer):
    reports = AttendanceReportSerializer(many=True)
    teacher = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = (
            'id',
            'date',
            'course',
            'teacher',
            'reports'
        )

    def get_course(self, obj):
        return obj.course.name

    def get_teacher(self, obj):
        teacher = obj.course.teacher
        return f'{teacher.first_name} {teacher.email}'


class CourseDetailSerializer(serializers.ModelSerializer):
    students = CourseStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('name', 'teacher', 'students')


class StrictBooleanField(serializers.BooleanField):
    def to_internal_value(self, value):
        if value in ('true', 'Present', 'True', '1'):
            return True
        if value in ('false', 'Absent', 'False', '0'):
            return False
        self.fail('invalid', input=None)

    def to_representation(self, value):
        if value:
            return "Present"
        return "Absent"


class AttendanceReportPostSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=30)
    status = StrictBooleanField(required=True)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        return instance

    def create(self, validated_data):
        pass


class AttendancePostSerializer(serializers.ModelSerializer):
    reports = AttendanceReportPostSerializer(many=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    def update(self, instance, validated_data):
        reports_data = validated_data.pop('reports')
        reports = instance.reports.all()
        reports = list(reports)
        instance.date = validated_data.get('date', instance.date)
        instance.course = validated_data.get('course', instance.course)
        instance.save()
        for report_data in reports_data:
            report = reports.pop(0)
            report.status = report_data.get('status', report.status)
            report.save()
        return instance

    def create(self, validated_data):
        report_list = validated_data.pop('reports')
        attendance = Attendance.objects.create(**validated_data)
        for student in report_list:
            student_obj = User.objects.get(id=student['student_id'])
            AttendanceReport.objects.create(attendance=attendance, student=student_obj, status=student['status'])
        return attendance

    class Meta:
        model = Attendance
        fields = (
            'id',
            'date',
            'course',
            'reports'
        )
