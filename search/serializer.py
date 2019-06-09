from rest_framework import serializers
from export.models import Meeting


class MeetingSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = [
            'name', 'skey', 'created_at'
        ]
