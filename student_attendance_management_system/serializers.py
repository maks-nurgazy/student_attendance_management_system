from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

from users.models import User
from .models import Course, Attendance, AttendanceReport


def add_subject_student(student_list, course):
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


class StatusBooleanField(serializers.BooleanField):
    def to_internal_value(self, value):
        value = str(value).lower()
        if value in ('true', 'present', '1'):
            return True
        if value in ('false', 'absent', '0'):
            return False
        self.fail('invalid', input=None)

    def to_representation(self, value):
        if value:
            return "Present"
        return "Absent"


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

    class Meta:
        model = Course
        fields = (
            'course_id',
            'name',
            'teacher',
            'students'
        )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        student_list = validated_data.pop('students', None)
        teacher_id = validated_data.pop('teacher', None)
        if (student_list is not None) and (teacher_id is not None):
            course = Course.objects.create(**validated_data, teacher=teacher_id)
            add_subject_student(student_list=student_list, course=course)
        elif (student_list is None) and (teacher_id is not None):
            course = Course.objects.create(**validated_data, teacher=teacher_id)
        elif (student_list is not None) and (teacher_id is None):
            course = Course.objects.create(**validated_data)
            add_subject_student(student_list=student_list, course=course)
        else:
            course = Course.objects.create(**validated_data)
        return Course.objects.get(id=course.id)

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


class StudentCourseSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    course_list = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Course.objects.all())

    def update(self, instance, validated_data):
        course_list = validated_data.get('course_list', instance.student_courses)
        instance.student_courses.clear()
        for course in course_list:
            instance.student_courses.add(course)
        instance.save()
        return instance

    def create(self, validated_data):
        pass

    class Meta:
        model = Course
        fields = (
            'name',
            'course_list'
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    students = CourseStudentSerializer(many=True)

    class Meta:
        model = Course
        fields = ('name', 'teacher', 'students')

    def update(self, instance, validated_data):
        student_list = validated_data.pop('students', None)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.name = validated_data.get('name', instance.name)
        if student_list is not None:
            instance.students.clear()
            add_subject_student(student_list=student_list, course=instance)
        instance.save()
        return instance


class CourseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
        )
        read_only_fields = [f.name for f in User._meta.get_fields()]


class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True, required=False)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exits")])

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        extra_kwargs = {'first_name': {'required': True}, }

    def to_internal_value(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        if not first_name:
            raise serializers.ValidationError({
                'first_name': "This field is required."
            })
        if not last_name:
            raise serializers.ValidationError({
                'last_name': 'This field is required.'
            })

        if not password and self.context['request'].method == 'POST':
            raise serializers.ValidationError({
                'password': 'This field is required.'
            })

        return super(TeacherSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        teacher = User.objects.create_teacher(**validated_data)
        return teacher

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class StudentSerializer(TeacherSerializer):
    def create(self, validated_data):
        student = User.objects.create_student(**validated_data)
        return student


class AttendanceReportSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    student_id = serializers.CharField(max_length=30, write_only=True)
    status = StatusBooleanField(required=True)

    class Meta:
        model = AttendanceReport
        fields = (
            'student',
            'student_id',
            'status',
        )

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        return instance

    def create(self, validated_data):
        pass

    def get_student(self, obj):
        query_set = obj.student
        return CourseStudentSerializer(query_set).data


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
            'reports',
        )

    def create(self, validated_data):
        report_list = validated_data.pop('reports')
        course = Course.objects.get(name=self.context.get('course_name'))
        user = self.context.get('user')
        if user.role == 2:
            if course.teacher.email != user.email:
                raise APIException('Your have not permission to do this action', code=status.HTTP_400_BAD_REQUEST)
        course_students = course.students
        attendance = Attendance.objects.create(**validated_data, course=course)
        for student in report_list:
            try:
                student_obj = course_students.get(id=student['student_id'])
                AttendanceReport.objects.create(attendance=attendance, student=student_obj, status=student['status'])
            except ObjectDoesNotExist:
                raise APIException(f'Student with id {student["student_id"]}, does not take this course', code=404)
        return attendance

    def update(self, instance, validated_data):
        reports_list = validated_data.pop('reports', None)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        if reports_list is not None:
            for student_data in reports_list:
                report = instance.reports.get(student=student_data['student_id'])
                report.status = student_data['status']
                report.save()
        return instance

    def get_teacher(self, obj):
        teacher = obj.course.teacher
        return CourseTeacherSerializer(teacher).data

    def get_course(self, obj):
        return obj.course.name
