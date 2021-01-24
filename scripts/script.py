import json

import requests

ENDPOINT = 'http://127.0.0.1:8000/api/'

login_url = ENDPOINT + 'auth/login/'
course_url = ENDPOINT + 'courses/'


def attendance_url(subject, attendance_id):
    return f'{ENDPOINT}{subject}/attendance/{attendance_id}'


def get_token(data=None):
    if data is None:
        data = {'email': 'admin@test.com', 'password': 'admin'}
    response = requests.request('post', login_url, data=data)
    response_obj = json.loads(response.text)
    return response_obj['access']


def add_course_as_admin(access_token):
    data = {
        "name": "Eders",
        "teacher": 6,
        "students": [
            {
                "id": 2,
                "email": "student@test.com",
                "role": 3
            },
            {
                "id": 5,
                "email": "student4@test.com",
                "role": 3
            }
        ]
    }
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json',
    }
    data = json.dumps(data)
    response = requests.request('post', course_url, data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'admin@test.com', 'password': 'admin'})
# add_course_as_admin(token)

def update_attendance_as_teacher(access_token):
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
    response = requests.request('put', attendance_url('Eders', 2), data=data, headers=headers)
    print(response.text)


# token = get_token(data={'email': 'teacher1@test.com', 'password': 'teacher'})
# update_attendance_as_teacher(token)


def delete_attendance_as_teacher(access_token, attendance_id):
    headers = {
        'Authorization': f'JWT {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.delete(attendance_url('Eders', attendance_id), headers=headers)
    print(response.text)


# token = get_token(data={'email': 'teacher1@test.com', 'password': 'teacher'})
# delete_attendance_as_teacher(token, 18)
