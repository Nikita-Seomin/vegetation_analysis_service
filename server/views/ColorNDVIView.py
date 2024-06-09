from rest_framework.views import APIView

from django.http import HttpResponse

from server.functions.Indexes.getColorNDVI import *
from server.models import InputFile
from server.serializers import InputFileSerializer

class getColorNDVIAPIView(APIView):

    def post(self, request):
        try:
            post_zip = InputFile.objects.create(
                upload=request.data['inputZip'],
            )

            zipFilePath = InputFileSerializer(post_zip).data['upload'][1:]
            fileLocation = getColorNDVI(zipFilePath)

            with open(fileLocation, 'rb') as f:
                file_data = f.read()

                # sending response
            response = HttpResponse(file_data, content_type='image/tiff')
            response['Content-Disposition'] = 'form-data; filename="NDVI.tiff"'

            return response

        except OSError:
            raise RuntimeError("unable to handle error")