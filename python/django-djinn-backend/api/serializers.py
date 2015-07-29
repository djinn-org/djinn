from rest_framework import serializers
from djinn.models import Room, Reservation, Equipment
from datetime import timedelta


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
        minutes = data.get('minutes')

        if end and minutes:
            raise serializers.ValidationError('Use either of these fields but not both: minutes, end')

        if end:
            if not start < end:
                raise serializers.ValidationError('start date-time must be before end date-time')
            minutes = (end - start).seconds / 60
        elif minutes:
            end = start + timedelta(minutes=minutes)
        else:
            raise serializers.ValidationError('Either field is required: minutes, end')

        return data


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
