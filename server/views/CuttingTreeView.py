from rest_framework.views import APIView

from django.http import HttpResponse

from server.functions.Indexes.getGIGreen import GIGreen
from server.functions.Indexes.getHSI import HSI
from server.functions.common import getPathToTrueColorFromZip
from server.functions.Indexes.getColorNDVI import *
from server.functions.getTreeMask import getTreeMask
from server.models import InputFile
from server.serializers import InputFileSerializer

class getCuttingTreeImageAPIView(APIView):

    def post(self, request):
        post_zip = InputFile.objects.create(
            upload=request.data['inputZip'],
        )

        zipFilePath = InputFileSerializer(post_zip).data['upload'][1:]

        trueFilePath = getPathToTrueColorFromZip(zipFilePath)
        # print(trueFilePath)
        maskFilePath = getTreeMask(trueFilePath)

        with open(trueFilePath, 'rb') as f:
            file_data = f.read()

            # sending response
        response = HttpResponse(file_data, content_type='image/tiff')
        response['Content-Disposition'] = 'form-data; filename="mask.tiff"'

        return response
