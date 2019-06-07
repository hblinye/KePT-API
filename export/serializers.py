from rest_framework import serializers
from rest_framework import fields


class ExportSerializer(serializers.Serializer):
    id = fields.IntegerField(read_only=True)