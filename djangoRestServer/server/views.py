from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .functions.getNDVI import NDVI


# Create your views here.


class ZipFileAPIView(APIView):
    def post(self, request):
        NDVI()

        respData= {
        'const': 1,
        }
        return Response(respData)
