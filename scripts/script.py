import json

import requests

ENDPOINT = 'http://127.0.0.1:8000/api/'

login_url = ENDPOINT + 'auth/login/'


def get_token(data=None):
    if data is None:
        data = {'email': 'admin@test.com', 'password': 'admin'}
    response = requests.request('post', login_url, data=data)
    response_obj = json.loads(response.text)
    return response_obj['access']


###################################################
#           Checking COURSE Model                 #
###################################################

# Course URLS

course_url = ENDPOINT + 'courses/'


def course_detail_url(course_id):
    return f'{course_url}{course_id}/'


###################################################


def add_course_all_as_admin(access_token):
    """ Adding a course with set Teacher and students as ADMIN"""

    data = {
        "name": "baha",
        "teacher": 3,
        "students": [
            {
                "email": "student322222@test.com",
                "first_name": "testStudent4",
                "last_name": "Test4",
                "password": "student"
            },
        ]
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    response = requests.request('post', course_url, data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# add_course_all_as_admin(token)


def add_course_without_students(access_token):
    """ Adding a course without setting students as ADMIN"""

    data = {
        "name": "math",
        "teacher": 3
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    response = requests.request('post', course_url, data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# add_course_without_students(token)


def add_course_without_teacher_and_students(access_token):
    """ Adding a course just setting course name as ADMIN"""

    data = {
        "name": "math"
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    response = requests.request('post', course_url, data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# add_course_without_teacher_and_students(token)


def delete_course_as_admin(access_token, course_id):
    headers = {
        'Authorization': f'JWT {access_token}'
    }
    response = requests.request('delete', course_detail_url(course_id), headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# delete_course_as_admin(token, 11)

def delete_course_in_range_as_admin(access_token, range_from, range_to):
    for i in range(range_from, range_to):
        delete_course_as_admin(access_token, i)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# delete_course_in_range_as_admin(token, 1, 20)


def update_course_teacher_as_admin(access_token, course_id):
    data = {
        "teacher": 2
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    response = requests.request('put', course_detail_url(course_id), data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# update_course_teacher_as_admin(token, 2)


def update_course_detail_as_admin(access_token, course_id):
    data = {
        "name": "mathematics"
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    response = requests.request('put', course_detail_url(course_id), data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# update_course_detail_as_admin(token, 2)


def update_course_students_as_admin(access_token, course_id):
    data = {
        'students': [
            {
                "id": 6,
                "first_name": "testStudent3",
                "last_name": "Test3",
                "email": "student3@test.com",
                "role": 3
            },
            {
                "id": 7,
                "first_name": "testStudent4",
                "last_name": "Test4",
                "email": "student4@test.com",
                "role": 3
            },
            {
                "id": 8,
                "first_name": "testStudent4",
                "last_name": "Test4",
                "email": "student5@test.com",
                "role": 3
            },
            {
                "id": 9,
                "first_name": "testStudent4",
                "last_name": "Test4",
                "email": "student32@test.com",
                "role": 3
            },
        ]
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    response = requests.request('put', course_detail_url(course_id), data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# update_course_students_as_admin(token, 2)


###################################################
#           Checking ATTENDANCE Model             #
###################################################

# Attendance URLS

def attendance_url(course_name):
    return f'{ENDPOINT}{course_name}/attendance/'


def attendance_detail_url(course_name, attendance_id):
    return f'{ENDPOINT}{course_name}/attendance/{attendance_id}'


####################################################

def post_attendance_as_teacher(access_token, course_name):
    data = {
        "date": "2050-10-31T11:30:00.511Z",
        "course": 45,
        "reports": [
            {
                "student_id": "2",
                "status": "Absent"
            },
            {
                "student_id": "5",
                "status": "Absent"
            }
        ]
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json',
    }
    data = json.dumps(data)
    response = requests.request('post', attendance_url(course_name), data=data, headers=headers)
    print(response.text)


token = get_token(data={'email': 'teacher1@test.com', 'password': 'teacher'})
post_attendance_as_teacher(token, 'mathematics')


def update_attendance_as_teacher(access_token, course_name):
    data = {
        "date": "2050-10-31T11:30:00.511Z",
        "course": 2,
        "reports": [
            {
                "student_id": "2",
                "status": "Absent"
            },
            {
                "student_id": "5",
                "status": "Absent"
            }
        ]
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json',
    }
    data = json.dumps(data)
    response = requests.request('put', attendance_detail_url(course_name, 2), data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'teacher1@test.com', 'password': 'teacher'})
# update_attendance_as_teacher(token, 'mathematics')


def delete_attendance_as_teacher(access_token, attendance_id):
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.delete(attendance_url('Eders', attendance_id), headers=headers)
    print(response.text)

# token = get_token(data={'email': 'teacher1@test.com', 'password': 'teacher'})
# delete_attendance_as_teacher(token, 18)
