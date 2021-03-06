# Generated by Django 3.1.5 on 2021-01-22 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_attendance_management_system', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='teacher_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendancereport',
            name='attendance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_attendance_management_system.attendance'),
        ),
        migrations.AddField(
            model_name='attendancereport',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='student_attendance_management_system.course'),
        ),
    ]
