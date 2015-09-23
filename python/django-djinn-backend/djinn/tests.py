from datetime import datetime, timedelta
import json
import unittest

from bs4 import BeautifulSoup
from django_djinn_backend import settings
import pytz
from django.utils import timezone
from django.test import TestCase
from django.test import Client
from djinn.models import Room, Building, Equipment, Reservation, Client as DjinnClient
from api.serializers import RoomSerializer, EquipmentSerializer, ReservationSerializer
from djinn.management.commands.rooms import Command as RoomCommand
from rest_framework import status


def to_json(serializer_cls, model_cls):
    return [serializer_cls(obj).data for obj in model_cls.objects.all()]


def to_json_first(serializer_cls, model_cls):
    return serializer_cls(model_cls.objects.all()[0]).data


def rooms_from_json(json_str):
    rooms = []
    for data in json.loads(json_str):
        room = Room.objects.get(pk=data['id'])
        rooms.append(room)
    return rooms


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


@unittest.skip("skip the test")
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

    def find_rooms(self, data):
        response = self.client.get('/api/v1/find/rooms/', data)
        self.assertEqual(response.status_code, 200)

        json_str = response.content.decode()
        return rooms_from_json(json_str)

    def test_find_rooms_with_computer(self):
        equipment_name = 'Computer'
        data = {
            'start': to_date_with_tz(datetime(2015, 8, 15, 11, 0)),
            'minutes': 30,
            'equipment': equipment_name,
        }
        rooms = self.find_rooms(data)
        self.assertTrue(len(rooms) > 0)

        for room in rooms:
            names = [re.equipment.name for re in room.roomequipment_set.all()]
            self.assertTrue(equipment_name in names)

    def test_find_rooms_with_computer_unavailable(self):
        equipment_name = 'Computer'
        data = {
            'start': to_date_with_tz(datetime(2015, 8, 15, 11, 0)),
            'minutes': 30,
            'equipment': equipment_name,
        }
        rooms = self.find_rooms(data)
        self.assertTrue(len(rooms) > 0)

        for room in rooms:
            names = [re.equipment.name for re in room.roomequipment_set.all()]
            self.assertTrue(equipment_name in names)

        rooms = self.find_rooms(data)
        self.assertTrue(len(rooms) > 0)

        for room in rooms:
            names = [re.equipment.name for re in room.roomequipment_set.all()]
            self.assertTrue(equipment_name in names)

    def test_find_rooms_with_computer_for_12(self):
        equipment_name = 'Computer'
        capacity_target = 12
        data = {
            'start': to_date_with_tz(datetime(2015, 8, 15, 11, 0)),
            'minutes': 30,
            'capacity': capacity_target,
            'equipment': equipment_name,
        }
        rooms = self.find_rooms(data)
        self.assertTrue(len(rooms) > 0)

        for room in rooms:
            self.assertTrue(room.capacity >= capacity_target)
            names = [re.equipment.name for re in room.roomequipment_set.all()]
            self.assertTrue(equipment_name in names)

    def test_find_rooms_with_phone_for_2(self):
        equipment_name = 'Phone'
        capacity_target = 2
        data = {
            'start': to_date_with_tz(datetime(2015, 8, 15, 11, 0)),
            'minutes': 30,
            'capacity': capacity_target,
            'equipment': equipment_name,
        }
        rooms = self.find_rooms(data)
        self.assertTrue(len(rooms) > 0)

        for room in rooms:
            self.assertTrue(room.capacity >= capacity_target)
            names = [re.equipment.name for re in room.roomequipment_set.all()]
            self.assertTrue(equipment_name in names)

    def test_find_rooms_with_phone_and_whiteboard(self):
        equipment_name1 = 'Phone'
        equipment_name2 = 'Whiteboard'
        data = {
            'start': to_date_with_tz(datetime(2015, 8, 15, 11, 0)),
            'minutes': 30,
            'equipment': '{},{}'.format(equipment_name1, equipment_name2),
        }
        rooms = self.find_rooms(data)
        self.assertTrue(len(rooms) > 0)

        for room in rooms:
            names = [re.equipment.name for re in room.roomequipment_set.all()]
            self.assertTrue(equipment_name1 in names)
            self.assertTrue(equipment_name2 in names)


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


class ImportRoomsTestCase(TestCase):
    room1_xml = '''<Rooms>
                <Room>
                    <Name>91A-13.E50(06)</Name>
                    <Mail>91A13E50@rc-its.credit-agricole.fr</Mail>
                    <Equipment>Room,TV,AudioConference,VideoConference,Computer</Equipment>
                    <Capacity>6</Capacity>
                    <Type>ResourceType:Room</Type>
                </Room>
            </Rooms>'''

    room2_xml = '''<Rooms>
                <Room>
                    <Name>91A-06.E29(06)</Name>
                    <Mail>91A06E29@rc-its.credit-agricole.fr</Mail>
                    <Equipment>Room,TV,AudioConference,VideoConference,VideoProjector</Equipment>
                    <Capacity>6</Capacity>
                    <Type>ResourceType:Room</Type>
                </Room>
            </Rooms>'''

    def setUp(self):
        self.cmd = RoomCommand()

    def test_import_room(self):
        soup = BeautifulSoup(self.room1_xml, 'html.parser')
        self.cmd.do_import_soup(soup)
        self.assertEquals(1, Room.objects.count())
        self.assertEquals(4, Equipment.objects.count())

        room = Room.objects.first()
        self.assertEquals(4, room.roomequipment_set.count())

    def test_import_room_twice_no_dups(self):
        soup = BeautifulSoup(self.room1_xml, 'html.parser')
        self.cmd.do_import_soup(soup)
        self.assertEquals(1, Room.objects.count())
        self.assertEquals(4, Equipment.objects.count())

        self.cmd.do_import_soup(soup)
        self.assertEquals(1, Room.objects.count())
        self.assertEquals(4, Equipment.objects.count())

    def test_import_two_rooms_with_overlap_in_equipment(self):
        soup = BeautifulSoup(self.room1_xml, 'html.parser')
        self.cmd.do_import_soup(soup)
        self.assertEquals(1, Room.objects.count())
        self.assertEquals(4, Equipment.objects.count())

        soup = BeautifulSoup(self.room2_xml, 'html.parser')
        self.cmd.do_import_soup(soup)
        self.assertEquals(2, Room.objects.count())
        self.assertEquals(5, Equipment.objects.count())

        def get_equipment_set(room):
            return {room.equipment for room in room.roomequipment_set.all()}

        room1, room2 = Room.objects.all()
        room1_equipment_set = get_equipment_set(room1)
        room2_equipment_set = get_equipment_set(room2)
        self.assertEquals(4, len(room1_equipment_set))
        self.assertEquals(4, len(room2_equipment_set))
        self.assertEquals(5, len(room1_equipment_set.union(room2_equipment_set)))


class ClientSanityTest(TestCase):
    def test_can_create_without_room_and_alias(self):
        # note: I wish these actually failed, as these are non-sense values
        DjinnClient.objects.create(mac='as', ip='', service_url='1')
        DjinnClient.objects.create(mac='as2', ip='2', service_url='2')


class ClientHeartbeatSanityTest(TestCase):
    def test_new_client_auto_creates_heartbeat(self):
        client = DjinnClient.objects.create(ip='', mac='')
        self.assertIsNotNone(client.clientheartbeat.last_heartbeat)

    def test_new_heartbeat(self):
        client = DjinnClient.objects.create(ip='', mac='')
        client.received_heartbeat()
        self.assertIsNotNone(client.clientheartbeat.last_heartbeat)

    def test_update_heartbeat(self):
        client = DjinnClient.objects.create(ip='', mac='')
        client.received_heartbeat()
        heartbeat1 = client.clientheartbeat.last_heartbeat
        client.received_heartbeat()
        heartbeat2 = client.clientheartbeat.last_heartbeat
        self.assertTrue(heartbeat1 < heartbeat2)


class ClientUpdateSanityTest(TestCase):
    def test_new_client_auto_creates_updates_with_zero_count(self):
        client = DjinnClient.objects.create(ip='', mac='')
        self.assertEqual(0, client.clientupdate.failed_updates)

    def test_increment_failed_updates(self):
        client = DjinnClient.objects.create(ip='', mac='')
        client.increment_failed_updates()
        self.assertEqual(1, client.clientupdate.failed_updates)
        client.increment_failed_updates()
        self.assertEqual(2, client.clientupdate.failed_updates)

    def test_clear_failed_updates(self):
        client = DjinnClient.objects.create(ip='', mac='')
        client.increment_failed_updates()
        self.assertEqual(1, client.clientupdate.failed_updates)
        client.clear_failed_updates()
        self.assertEqual(0, client.clientupdate.failed_updates)


class ClientPresenceTest(TestCase):
    def setUp(self):
        self.client = Client()

    def client_presence(self, mac):
        return self.client.put('/api/v1/clients/{}/presence'.format(mac))

    def test_invalid_mac(self):
        response = self.client_presence('x')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def extract_error_msg(self, response):
        return json.loads(response.content.decode())['error']

    def test_no_such_client(self):
        response = self.client_presence('aa:bb:cc:dd:ee:ff')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals('No such client', self.extract_error_msg(response))

    def test_no_associated_room(self):
        mac = 'aa:bb:cc:dd:ee:ff'
        DjinnClient.objects.create(mac=mac, ip='x')
        response = self.client_presence(mac)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals('No associated room', self.extract_error_msg(response))

    def test_room_not_available(self):
        building = Building.objects.create()
        room = Room.objects.create(building=building, floor=1, capacity=1)
        mac = 'aa:bb:cc:dd:ee:ff'
        DjinnClient.objects.create(mac=mac, ip='x', room=room)
        Reservation.objects.create(room=room, start=timezone.now(), minutes=30)

        response = self.client_presence(mac)
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEquals('Room is not available', self.extract_error_msg(response))


class RoomAvailableTest(TestCase):
    def setUp(self):
        self.building = Building.objects.create()
        self.room = Room.objects.create(building=self.building, floor=1, capacity=1)

    def test_available_when_no_meetings(self):
        self.assertTrue(self.room.is_available())

    def test_not_available_if_meeting_starts_now(self):
        start = timezone.now()
        Reservation.objects.create(room=self.room, start=start, minutes=30)
        self.assertFalse(self.room.is_available())

    def test_not_available_if_next_meeting_within_wait_period(self):
        start = timezone.now() + settings.WAIT_DELTA
        Reservation.objects.create(room=self.room, start=start, minutes=30)
        self.assertFalse(self.room.is_available())

    def test_not_available_if_during_meeting(self):
        start = timezone.now() - timedelta(minutes=5)
        Reservation.objects.create(room=self.room, start=start, minutes=30)
        self.assertFalse(self.room.is_available())

    def test_available_if_next_meeting_beyond_wait_period(self):
        start = timezone.now() + settings.WAIT_DELTA + timedelta(minutes=1)
        Reservation.objects.create(room=self.room, start=start, minutes=30)
        self.assertTrue(self.room.is_available())

    def test_available_if_beyond_end_of_prev_meeting(self):
        minutes = 30
        start = timezone.now() - timedelta(minutes=minutes)
        Reservation.objects.create(room=self.room, start=start, minutes=minutes)
        self.assertTrue(self.room.is_available())
