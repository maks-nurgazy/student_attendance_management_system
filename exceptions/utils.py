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
        # else:
        #     dict_response = response.data
        #     key = list(dict_response.keys())[0]
        #     print(dict_response)
        #     obj = dict_response[key]
        #     data['message'] = str(exc)
        #     if obj.code == 'method_not_allowed':
        #         data['status_code'] = 405
        #         response.status_code = 405
        #     else:
        #         data['status_code'] = obj.code
        #         response.status_code = obj.code
        # response.data = data
    return response


def custom404(request, exception=None):
    data = {
        "success": False,
        "message": "Requested url not found",
        "status_code": status.HTTP_404_NOT_FOUND
    }
    return JsonResponse(data=data)
