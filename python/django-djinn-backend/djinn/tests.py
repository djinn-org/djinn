from django.test import TestCase
from django.test import Client
from djinn.models import Room, Building, Equipment
from api.serializers import RoomSerializer, EquipmentSerializer
import json


def to_json(serializer_cls, model_cls):
    return [serializer_cls(obj).data for obj in model_cls.objects.all()]


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

        json = response.content.decode()
        self.assertJSONEqual(json, to_json(RoomSerializer, Room))


class EquipmentListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.pc = Equipment.objects.create(name="PC")
        self.phone = Equipment.objects.create(name="Phone")

    def test_list_equipment(self):
        response = self.client.get('/api/v1/equipments/')
        self.assertEqual(response.status_code, 200)

        json = response.content.decode()
        self.assertJSONEqual(json, to_json(EquipmentSerializer, Equipment))


class FindRoomsTestCase(TestCase):
    pass


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
        # TODO: should also report missing end / duration

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

    def test_reserve_ok_sanity(self):
        pass

    def test_reserve_fails_if_missing_end_and_duration(self):
        pass

    def test_reserve_ok_with_start_and_duration(self):
        pass

    def test_reserve_ok_with_start_and_end(self):
        pass

    def test_reserve_fails_if_end_before_start(self):
        pass

