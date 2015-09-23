from datetime import timedelta
from django import forms
from django.utils import timezone
from django_djinn_backend import settings
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from djinn.models import Room, Reservation, Equipment, Client, ReservationLog
from api.serializers import RoomSerializer, ReservationSerializer, EquipmentSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FindRoomsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def list(self, request, room_id):
        reservations = Reservation.objects.filter(room_id=room_id)
        page = self.paginate_queryset(reservations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, room_id, pk):
        queryset = Reservation.objects.filter(room_id=room_id)
        reservation = get_object_or_404(queryset, pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class FindRoomsForm(forms.Form):
    start = forms.DateTimeField()
    end = forms.DateTimeField(required=False)
    capacity = forms.IntegerField(required=False)
    # TODO: equipment, some kind of multi-select


@api_view(['GET'])
def find_rooms(request):
    form = FindRoomsForm(request.data)
    debug = form.is_valid()
    # debug = dir(form)
    # debug = form.errors
    # debug = request.data
    return Response({"debug": debug})
    # return Response({"message": "hello", "data": request.data, "debug": debug})


def ext_sync_room(room):
    return room


def ext_reserve(room, start, end):
    pass


def ext_cancel(room, start, end):
    pass


@api_view(['PUT'])
def client_presence(request, mac):
    try:
        client = Client.objects.get(mac=mac)
    except Client.DoesNotExist:
        return Response({"error": "No such client"}, status=status.HTTP_400_BAD_REQUEST)

    room = client.room
    if not room:
        return Response({"error": "No associated room"}, status=status.HTTP_400_BAD_REQUEST)

    room = ext_sync_room(room)

    if room.is_available():
        minutes = min(settings.AUTO_RESERVATION_MINUTES, room.calc_minutes_to_next_reservation())
        start = timezone.now()
        end = start + timedelta(minutes=minutes)

        reservation = Reservation.objects.create(room=room, start=start, minutes=minutes)
        ReservationLog.create_from_reservation(reservation, ReservationLog.TYPE_CREATE, ReservationLog.TRIGGER_DJINN)

        ext_reserve(room, start, end)
        room = ext_sync_room(room)

        client.update_status(room.status)

        return Response({"message": "Room was available. Current status: {}".format(room.status)})

    return Response({"error": "Room is not available"}, status=status.HTTP_409_CONFLICT)

@api_view(['PUT'])
def client_empty(request, mac):
    try:
        client = Client.objects.get(mac=mac)
    except Client.DoesNotExist:
        return Response({"error": "No such client"}, status=status.HTTP_400_BAD_REQUEST)

    room = client.room
    if not room:
        return Response({"error": "No associated room"}, status=status.HTTP_400_BAD_REQUEST)

    room = ext_sync_room(room)

    if not room.is_available():
        reservation = room.get_current_reservation()
        if reservation:
            reservation.delete()
            ReservationLog.create_from_reservation(reservation, ReservationLog.TYPE_CANCEL, ReservationLog.TRIGGER_DJINN)

            ext_cancel(room, reservation.start, reservation.end)
            room = ext_sync_room(room)

            client.update_status(room.status)

            return Response({"message": "Room was booked. Current status: {}".format(room.status)})

    return Response({"error": "Room is empty"}, status=status.HTTP_409_CONFLICT)
