from rest_framework.exceptions import APIException
from rest_framework import status

class BaseServiceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Service error"
    default_code = "service_error"

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class ServiceException(BaseServiceException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Something went wrong"


class NotFoundException(BaseServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found"


class PermissionDeniedException(BaseServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Permission denied"