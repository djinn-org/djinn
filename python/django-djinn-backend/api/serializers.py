from rest_framework import serializers
from djinn.models import Room, Reservation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation

    def validate(self, attrs):
        data = super().validate(attrs)

        start = data.get('start')
        end = data.get('end')
        if not start < end:
            raise serializers.ValidationError('start date-time must be before end date-time')

        return data
