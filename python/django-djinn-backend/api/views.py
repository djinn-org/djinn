from datetime import timedelta
from django import forms
from django.utils import timezone
from django_djinn_backend import settings
from django_djinn_backend import exchange
from random import randint
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from djinn.models import Room, Reservation, Equipment, Client, ReservationLog
from api.serializers import RoomSerializer, ReservationSerializer, EquipmentSerializer, FindRoomResultSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FindRoomResult:
    def __init__(self, room, accuracy):
        self.room = room
        self.accuracy = accuracy


class FindRoomsViewSet(viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = FindRoomResultSerializer

    def list(self, request):
        # TODO: implement proper filtering
        results = [FindRoomResult(room, randint(80, 100)) for room in Room.objects.all()[:10]]
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


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


def merge_reservations(room, reservations):
    to_add = []

    for reservation in reservations:
        start = reservation['start']
        end = reservation['end']

        # delete any that starts before start and ends after start -> log it
        for to_delete in room.reservation_set.filter(start__lt=start, end__gt=start):
            ReservationLog.create_from_reservation(to_delete, ReservationLog.TYPE_CANCEL, ReservationLog.TRIGGER_EXT)
            to_delete.delete()

        # delete any that starts before end and ends after end -> log it
        for to_delete in room.reservation_set.filter(start__lt=end, end__gt=end):
            ReservationLog.create_from_reservation(to_delete, ReservationLog.TYPE_CANCEL, ReservationLog.TRIGGER_EXT)
            to_delete.delete()

        # delete any that starts after start and ends before end -> log it
        for to_delete in room.reservation_set.filter(start__gt=start, end__lte=end):
            ReservationLog.create_from_reservation(to_delete, ReservationLog.TYPE_CANCEL, ReservationLog.TRIGGER_EXT)
            to_delete.delete()

        # delete any that starts after start and ends before end -> log it
        for to_delete in room.reservation_set.filter(start__gte=start, end__lt=end):
            ReservationLog.create_from_reservation(to_delete, ReservationLog.TYPE_CANCEL, ReservationLog.TRIGGER_EXT)
            to_delete.delete()

        if not room.reservation_set.filter(start=start, end=end):
            to_add.append(reservation)

    for reservation in to_add:
        # after all reservation processed, add all that were set aside -> log it
        start = reservation['start']
        end = reservation['end']
        reservation = Reservation.objects.create(room=room, start=start, end=end)
        ReservationLog.create_from_reservation(reservation, ReservationLog.TYPE_CREATE, ReservationLog.TRIGGER_EXT)


def ext_sync_room(start, end, room):
    reservations = exchange.list_reservations(start, end, room)
    if reservations and room.external_name in reservations:
        merge_reservations(room, reservations[room.external_name])

    return room


def ext_create_reservation(start, end, room):
    exchange.create_reservation(start, end, room)


def ext_cancel_reservation(start, end, room):
    exchange.cancel_reservation(start, end, room)


def update_client_ip(client, request):
    orig_ip = client.ip
    ip = get_client_ip(request)
    if orig_ip != ip:
        client.ip = ip
        client.save()


@api_view(['PUT'])
def client_presence(request, mac):
    try:
        client = Client.objects.get(mac=mac)
    except Client.DoesNotExist:
        return Response({"error": "No such client"}, status=status.HTTP_400_BAD_REQUEST)

    update_client_ip(client, request)

    room = client.room
    if not room:
        return Response({"error": "No associated room"}, status=status.HTTP_400_BAD_REQUEST)

    if not client.enabled:
        return Response({"error": "Client disabled"}, status=status.HTTP_400_BAD_REQUEST)

    start = timezone.now()
    end = start + timedelta(minutes=settings.AUTO_RESERVATION_MINUTES)
    room = ext_sync_room(start, end, room)

    if room.is_available():
        minutes = min(settings.AUTO_RESERVATION_MINUTES, room.calc_minutes_to_next_reservation())
        end = start + timedelta(minutes=minutes)

        reservation = Reservation.objects.create(room=room, start=start, minutes=minutes)
        ReservationLog.create_from_reservation(reservation, ReservationLog.TYPE_CREATE, ReservationLog.TRIGGER_DJINN)

        ext_create_reservation(start, end, room)
        room = ext_sync_room(start, end, room)

        client.update_status(room.status)

        return Response({"message": "Room was available. Current status: {}".format(room.status)})

    return Response({"error": "Room is not available"}, status=status.HTTP_409_CONFLICT)

@api_view(['PUT'])
def client_empty(request, mac):
    try:
        client = Client.objects.get(mac=mac)
    except Client.DoesNotExist:
        return Response({"error": "No such client"}, status=status.HTTP_400_BAD_REQUEST)

    update_client_ip(client, request)

    room = client.room
    if not room:
        return Response({"error": "No associated room"}, status=status.HTTP_400_BAD_REQUEST)

    if not client.enabled:
        return Response({"error": "Client disabled"}, status=status.HTTP_400_BAD_REQUEST)

    start = timezone.now()
    end = start + timedelta(minutes=settings.AUTO_RESERVATION_MINUTES)
    room = ext_sync_room(start, end, room)

    if not room.is_available():
        reservation = room.get_current_reservation()
        if reservation:
            if reservation.start < timezone.now() - settings.WAIT_DELTA:
                reservation.delete()
                ReservationLog.create_from_reservation(reservation, ReservationLog.TYPE_CANCEL, ReservationLog.TRIGGER_DJINN)

                ext_cancel_reservation(reservation.start, reservation.end, room)
                room = ext_sync_room(start, end, room)

                client.update_status(room.status)

                return Response({"message": "Room was booked. Current status: {}".format(room.status)})

            else:
                return Response({"message": "Room is booked, but not canceling soon after start."}, status=status.HTTP_428_PRECONDITION_REQUIRED)

    return Response({"error": "Room is empty"}, status=status.HTTP_409_CONFLICT)


@api_view(['HEAD'])
def client_heartbeat(request, mac):
    try:
        Client.objects.get(mac=mac).received_heartbeat()
        return Response({}, status=status.HTTP_200_OK)
    except Client.DoesNotExist:
        return Response({"error": "No such client"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['ip', 'mac', 'alias', 'service_url']


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# TODO: move this to /clients
@api_view(['POST'])
def client_register(request, mac):
    ip = get_client_ip(request)
    request.POST['ip'] = ip
    request.POST['service_url'] = 'http://{}:8001/api/v1'.format(ip)
    try:
        client = Client.objects.get(mac=mac)
        form = RegisterClientForm(request.POST, instance=client)
    except Client.DoesNotExist:
        client = None
        form = RegisterClientForm(request.POST)

    if form.is_valid():
        form.save()
        if client:
            return Response({"message": "Updated client"})
        return Response({"message": "Register client OK"})

    return Response({"error": "Invalid parameters", "errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

