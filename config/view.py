from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

class HelloWorldView(APIView):
    @extend_schema(
        summary="Hello World Endpoint",
        description="A simple endpoint that returns a greeting message.",
        responses={200: {"message": "Hello, World!"}}
    )
    def get(self, request):
        return Response({"message": "Hello, World!"})