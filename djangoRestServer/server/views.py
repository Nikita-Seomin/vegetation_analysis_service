from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse, HttpResponseNotFound

from .functions.common import getPathToTrueColorFromZip, getPathToRedFromZip
from .functions.getNDVI import *
from .models import InputFile
from .serializers import InputFileSerializer, InputFileTrueColorSerializer


# Create your views here.


class ZipFileAPIView(APIView):
    def post(self, request):
        post_zip = InputFile.objects.create(
            upload=request.data['inputZip'],
        )

        zipFilePath = InputFileSerializer(post_zip).data['upload'][1:]
        # fileLocation = NDVI(zipFilePath)
        trueFilePath = getPathToTrueColorFromZip(zipFilePath)
        maskFilePath = getTreeMask(trueFilePath)

        with open(maskFilePath, 'rb') as f:
            file_data = f.read()

            # sending response
        response = HttpResponse(file_data, content_type='image/tiff')
        response['Content-Disposition'] = 'form-data; filename="mask.tiff"'

        return response
