# Generated by Django 3.1.5 on 2021-01-28 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_attendance_management_system', '0004_auto_20210124_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
