from rest_framework import serializers
from server.models import InputFile, ResultFile


class InputFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputFile
        fields = ('upload',)

        def get_photo_url(self, obj):
            request = self.context.get('request')
            zip_url = obj.fingerprint.url
            return request.build_absolute_uri(zip_url)


class ResultFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultFile
        fields = ('result_file',)

        def get_photo_url(self, obj):
            request = self.context.get('request')
            zip_url = obj.fingerprint.url
            return request.build_absolute_uri(zip_url)