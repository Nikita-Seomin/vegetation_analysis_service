from rest_framework import serializers
from server.models import InputFile, ResultFile, InputFileTrueColor


class InputFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputFile
        fields = ('upload',)

        def get_photo_url(self, obj):
            request = self.context.get('request')
            zip_url = obj.fingerprint.url
            return request.build_absolute_uri(zip_url)


class InputFileTrueColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputFileTrueColor
        fields = ('upload',)

        def get_photo_url(self, obj):
            request = self.context.get('request')
            image = obj.fingerprint.url
            return request.build_absolute_uri(image)


class ResultFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultFile
        fields = ('result_file',)

        def get_photo_url(self, obj):
            request = self.context.get('request')
            zip_url = obj.fingerprint.url
            return request.build_absolute_uri(zip_url)