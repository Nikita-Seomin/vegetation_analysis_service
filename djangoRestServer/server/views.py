from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .functions.getNDVI import NDVI
from .models import InputFile
from .serializers import InputFileSerializer


# Create your views here.


class ZipFileAPIView(APIView):
    def post(self, request):
        post_zip = InputFile.objects.create(
            upload=request.data['inputZip'],
        )

        zipFilePath = InputFileSerializer(post_zip).data['upload'][1:]
        print(zipFilePath)
        NDVI(zipFilePath)

        respData= {
        'const': 1,
        }
        return Response(respData)
