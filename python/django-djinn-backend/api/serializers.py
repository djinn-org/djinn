from rest_framework import serializers
from djinn.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
