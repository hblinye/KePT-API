from rest_framework import serializers
from rest_framework import fields
from .models import Thought


class ExportSerializer(serializers.Serializer):
    name = fields.CharField(read_only=True)
    _keep = fields.CharField(max_length=500)
    _problem = fields.CharField(max_length=500)
    _try = fields.CharField(max_length=500)

