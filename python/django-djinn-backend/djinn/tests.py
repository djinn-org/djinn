from datetime import datetime
import pytz
from django.utils import timezone
from django.test import TestCase
from django.test import Client
from djinn.models import Room, Building, Equipment, Reservation
from api.serializers import RoomSerializer, EquipmentSerializer, ReservationSerializer
import json


def to_json(serializer_cls, model_cls):
    return [serializer_cls(obj).data for obj in model_cls.objects.all()]


def to_json_first(serializer_cls, model_cls):
    return serializer_cls(model_cls.objects.all()[0]).data


def to_date_with_tz(dt):
    tz = timezone.get_default_timezone_name()
    return pytz.timezone(tz).localize(dt)


class RoomListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        building = Building.objects.create(name='main')

        Room.objects.create(
            building=building,
            floor=12,
            name='E50',
            capacity=8,
        )

        Room.objects.create(
            building=building,
            floor=16,
            name='J89',
            capacity=20,
        )

    def test_list_rooms(self):
        response = self.client.get('/api/v1/rooms/')
        self.assertEqual(response.status_code, 200)

        obj = response.content.decode()
        self.assertJSONEqual(obj, to_json(RoomSerializer, Room))


class EquipmentListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.pc = Equipment.objects.create(name="PC")
        self.phone = Equipment.objects.create(name="Phone")

    def test_list_equipment(self):
        response = self.client.get('/api/v1/equipments/')
        self.assertEqual(response.status_code, 200)

        obj = response.content.decode()
        self.assertJSONEqual(obj, to_json(EquipmentSerializer, Equipment))


class FindRoomsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        building = Building.objects.create(name='main')

        room1 = Room.objects.create(
            building=building,
            floor=12,
            name='E50',
            capacity=8,
        )
        Room.objects.create(
            building=building,
            floor=14,
            name='E17',
            capacity=4,
        )

        self.reservation = Reservation.objects.create(
            room=room1,
            start=to_date_with_tz(datetime(2015, 8, 15, 11, 0)),
            end=to_date_with_tz(datetime(2015, 8, 15, 12, 0)),
            minutes=60,
            # TODO: should not have to specify both end and minutes
        )

    def test_find_rooms_without_filters(self):
        response = self.client.get('/api/v1/find/rooms/')
        self.assertEqual(response.status_code, 200)

        obj = response.content.decode()
        self.assertJSONEqual(obj, to_json(RoomSerializer, Room))
        # TODO: use default date params

    def test_find_rooms_with_filters(self):
        # TODO: derive conflicting params from the known reservation
        data = {
            'start': to_date_with_tz(datetime(2015, 8, 15, 11, 0)),
            'minutes': 30,
        }
        response = self.client.get('/api/v1/find/rooms/', data)
        self.assertEqual(response.status_code, 200)

        obj = response.content.decode()
        # TODO: fabricate conditions to match only one room
        self.assertJSONEqual(obj, to_json(RoomSerializer, Room))


class MakeReservationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        building = Building.objects.create(name='main')

        Room.objects.create(
            building=building,
            floor=12,
            name='E50',
            capacity=8,
        )

    def test_reserve_fails_if_missing_start_or_room(self):
        response = self.client.post('/api/v1/reservations/')
        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content.decode())
        errormsg = ['This field is required.']
        self.assertEqual(content['room'], errormsg)
        self.assertEqual(content['start'], errormsg)
        self.assertEqual(len(content), 2)
        # TODO: should also report missing end / minutes

    def test_reserve_fails_if_missing_room(self):
        data = {'room': 1}
        response = self.client.post('/api/v1/reservations/', data)
        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content.decode())
        errormsg = ['This field is required.']
        self.assertEqual(content['start'], errormsg)
        self.assertEqual(len(content), 1)

    def test_reserve_fails_if_invalid_room(self):
        data = {'room': 11}
        response = self.client.post('/api/v1/reservations/', data)
        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content.decode())
        errormsg = ['This field is required.']
        self.assertEqual(content['start'], errormsg)
        self.assertTrue(content['room'][0].startswith('Invalid pk '))
        self.assertEqual(len(content), 2)

    def test_reserve_fails_if_no_room_no_start(self):
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 400)

        obj = json.loads(response.content.decode())
        self.assertTrue('non_field_errors' in obj)

    def test_reserve_ok_with_start_and_minutes(self):
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'minutes': 15,
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 201)

        obj = response.content.decode()
        self.assertJSONEqual(obj, to_json_first(ReservationSerializer, Reservation))

    def test_reserve_ok_with_start_and_end(self):
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'end': '2015-07-27T13:00',
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 201)

        obj = response.content.decode()
        self.assertJSONEqual(obj, to_json_first(ReservationSerializer, Reservation))

    def test_reserve_fails_if_end_before_start(self):
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'end': '2015-07-27T11:00',
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 400)

        obj = json.loads(response.content.decode())
        self.assertTrue('non_field_errors' in obj)

    def test_reserve_fails_if_start_overlaps(self):
        room = Room.objects.all()[0]
        start = to_date_with_tz(datetime(2015, 7, 27, 11, 50))
        Reservation.objects.create(room=room, start=start, minutes=15)
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'minutes': 15,
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 400)

        obj = json.loads(response.content.decode())
        self.assertTrue('non_field_errors' in obj)

    def test_reserve_fails_if_end_overlaps(self):
        room = Room.objects.all()[0]
        start = to_date_with_tz(datetime(2015, 7, 27, 12, 10))
        Reservation.objects.create(room=room, start=start, minutes=15)
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'minutes': 15,
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 400)

        obj = json.loads(response.content.decode())
        self.assertTrue('non_field_errors' in obj)

    def test_reserve_fails_if_existing_within_start_end(self):
        room = Room.objects.all()[0]
        start = to_date_with_tz(datetime(2015, 7, 27, 12, 5))
        Reservation.objects.create(room=room, start=start, minutes=5)
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'minutes': 15,
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 400)

        obj = json.loads(response.content.decode())
        self.assertTrue('non_field_errors' in obj)

    def test_reserve_fails_if_start_end_within_existing(self):
        room = Room.objects.all()[0]
        start = to_date_with_tz(datetime(2015, 7, 27, 11, 55))
        Reservation.objects.create(room=room, start=start, minutes=30)
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'minutes': 15,
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 400)

        obj = json.loads(response.content.decode())
        self.assertTrue('non_field_errors' in obj)

    def test_reserve_ok_just_before_existing(self):
        room = Room.objects.all()[0]
        start = to_date_with_tz(datetime(2015, 7, 27, 13, 0))
        first = Reservation.objects.create(room=room, start=start, minutes=30)
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'end': '2015-07-27T13:00',
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 201)

        first.delete()
        obj = response.content.decode()
        self.assertJSONEqual(obj, to_json_first(ReservationSerializer, Reservation))

    def test_reserve_ok_just_after_existing(self):
        room = Room.objects.all()[0]
        start = to_date_with_tz(datetime(2015, 7, 27, 11, 0))
        first = Reservation.objects.create(room=room, start=start, minutes=60)
        data = {
            'room': 1,
            'start': '2015-07-27T12:00',
            'end': '2015-07-27T13:00',
        }
        response = self.client.post('/api/v1/reservations/', data=data)
        self.assertEqual(response.status_code, 201)

        first.delete()
        obj = response.content.decode()
        self.assertJSONEqual(obj, to_json_first(ReservationSerializer, Reservation))
