from django import forms
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from djinn.models import Room, Reservation, Equipment
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
    end = forms.DateTimeField()
    capacity = forms.IntegerField(required=False)
    # TODO: equipment, some kind of multi-select


@api_view(['GET'])
def find_rooms(request):
    pass
    # form = FindRoomsForm(request.data)
    # debug = form.is_valid()
    # debug = dir(form)
    # debug = form.errors
    # debug = request.data
    # return Response({"debug": debug})
    # return Response({"message": "hello", "data": request.data, "debug": debug})
