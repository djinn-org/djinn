from rest_framework import serializers
from djinn.models import Room, Reservation, Equipment, IllegalReservation
from datetime import timedelta


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room


class FindRoomResultSerializer(serializers.Serializer):
    room = RoomSerializer()
    accuracy = serializers.IntegerField()


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation

    def validate(self, attrs):
        data = super().validate(attrs)

        room = data.get('room')
        start = data.get('start')
        end = data.get('end')
        minutes = data.get('minutes')

        if end and minutes:
            raise serializers.ValidationError('Use either of these fields but not both: minutes, end')

        if end:
            if not start < end:
                raise serializers.ValidationError('start date-time must be before end date-time')
            minutes = (end - start).seconds / 60
            data['minutes'] = minutes
        elif minutes:
            end = start + timedelta(minutes=minutes)
            data['end'] = end
        else:
            raise serializers.ValidationError('Either field is required: minutes, end')

        if Reservation.objects.filter(room=room, start__lt=start, end__gt=start).exists():
            raise serializers.ValidationError('Reservation overlaps with existing')
        if Reservation.objects.filter(room=room, start__lt=end, end__gt=end).exists():
            raise serializers.ValidationError('Reservation overlaps with existing')
        if Reservation.objects.filter(room=room, start__gt=start, end__lte=end).exists():
            raise serializers.ValidationError('Reservation overlaps with existing')
        if Reservation.objects.filter(room=room, start__gte=start, end__lt=end).exists():
            raise serializers.ValidationError('Reservation overlaps with existing')
        if Reservation.objects.filter(room=room, start=start, end=end).exists():
            raise serializers.ValidationError('Reservation overlaps with existing')

        return data


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
