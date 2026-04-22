from rest_framework.exceptions import APIException
from rest_framework import status


class ServiceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Something went wrong"


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found"


class PermissionDeniedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Permission denied"