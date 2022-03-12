from rest_framework import serializers
from .convert import ALLOW_CONVERT
from django.conf import settings
import os

class ConvertQueryParamSerializer(serializers.Serializer):

    target_ext = serializers.CharField(max_length=200, allow_null=False)
    origin_filename = serializers.CharField(max_length=200, allow_null=False)

    def validate_target_ext(self, value):
        if not value.upper() in [_.target for _ in ALLOW_CONVERT]:
            raise serializers.ValidationError(f"{value} not allow")
        return value
    
    def validate_origin_filename(self, value):
        filename = f"{settings.MEDIA_ROOT}/{value}"

        if not os.path.exists(filename):
            raise serializers.ValidationError(f"{value} not exists")
        return value