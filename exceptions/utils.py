from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        data = {
            "success": False,
            "message": "Error",
            "status_code": response.status_code
        }
        if response.status_code == 404:
            data['message'] = "Not Found"
        elif response.status_code == 401:
            data['message'] = "Unauthorized"
        else:
            obj = response.data['detail']
            data['message'] = str(exc)
            response.status_code = obj.code
            data['status_code'] = obj.code
        response.data = data
    return response


def custom404(request, exception=None):
    data = {
        "success": False,
        "message": "Requested url not found",
        "status_code": status.HTTP_404_NOT_FOUND
    }
    return JsonResponse(data=data)
