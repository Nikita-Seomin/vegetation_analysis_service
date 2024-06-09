
from rest_framework.views import APIView

from django.http import HttpResponse

from server.functions.Indexes.getGIGreen import GIGreen
from server.functions.getHogweed import Hoogweed
from server.models import InputFile
from server.serializers import InputFileSerializer

class getHoogweedAPIView(APIView):

    def post(self, request):
        post_zip = InputFile.objects.create(
            upload=request.data['inputZip'],
        )

        zipFilePath = InputFileSerializer(post_zip).data['upload'][1:]
        fileLocation = Hoogweed(zipFilePath)
        # trueFilePath = getPathToTrueColorFromZip(zipFilePath)
        # maskFilePath = getTreeMask(trueFilePath)

        with open(fileLocation, 'rb') as f:
            file_data = f.read()

            # sending response
        response = HttpResponse(file_data, content_type='image/tiff')
        response['Content-Disposition'] = 'form-data; filename="GIGreen.tiff"'

        return response