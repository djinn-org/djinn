from datetime import datetime, timedelta
import json
import unittest

from api.views import merge_reservations

from django_djinn_backend.exchange import run_cmd, list_reservations, parse_reservations, parse_date

from bs4 import BeautifulSoup
from django_djinn_backend import settings
import pytz
from django.utils import timezone
from django.test import TestCase
from django.test import Client
from djinn.models import Room, Building, Equipment, Reservation, Client as DjinnClient, ReservationLog
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


def create_dummy_room():
    return Room.objects.create(
        building=Building.objects.create(name='main'),
        floor=12,
        name='E50',
        external_name='E50',
        capacity=8,
    )


class RoomListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        building = Building.objects.create(name='main')

        Room.objects.create(
            building=building,
            floor=12,
            name='E50',
            external_name='E50',
            capacity=8,
        )

        Room.objects.create(
            building=building,
            floor=16,
            name='J89',
            external_name='J89',
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

    def client_empty(self, mac):
        return self.client.put('/api/v1/clients/{}/empty'.format(mac))

    def test_invalid_mac(self):
        response = self.client_presence('x')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def extract_error_msg(self, response):
        return json.loads(response.content.decode())['error']

    def extract_msg(self, response):
        return json.loads(response.content.decode())['message']

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

    def test_reserve_success(self):
        building = Building.objects.create()
        room = Room.objects.create(building=building, floor=1, capacity=1)
        mac = 'aa:bb:cc:dd:ee:ff'
        client = DjinnClient.objects.create(mac=mac, ip='x', room=room)

        self.assertEquals(0, ReservationLog.objects.count())
        self.assertEquals(0, client.clientupdate.failed_updates)

        response = self.client_presence(mac)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEquals('Room was available. Current status: OCCUPIED', self.extract_msg(response))

        self.assertEquals(1, ReservationLog.objects.count())
        client.clientupdate.refresh_from_db()
        self.assertEquals(1, client.clientupdate.failed_updates)

    def test_cancel_success(self):
        building = Building.objects.create()
        room = Room.objects.create(building=building, floor=1, capacity=1)
        mac = 'aa:bb:cc:dd:ee:ff'
        client = DjinnClient.objects.create(mac=mac, ip='x', room=room)
        start = timezone.now() - settings.WAIT_DELTA
        Reservation.objects.create(room=room, start=start, minutes=30)

        self.assertEquals(0, ReservationLog.objects.count())
        self.assertEquals(0, client.clientupdate.failed_updates)

        response = self.client_empty(mac)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEquals('Room was booked. Current status: FREE', self.extract_msg(response))

        self.assertEquals(1, ReservationLog.objects.count())
        client.clientupdate.refresh_from_db()
        self.assertEquals(1, client.clientupdate.failed_updates)

    def test_dont_cancel_too_soon_after_start(self):
        building = Building.objects.create()
        room = Room.objects.create(building=building, floor=1, capacity=1)
        mac = 'aa:bb:cc:dd:ee:ff'
        client = DjinnClient.objects.create(mac=mac, ip='x', room=room)
        Reservation.objects.create(room=room, start=timezone.now(), minutes=30)

        self.assertEquals(0, ReservationLog.objects.count())
        self.assertEquals(0, client.clientupdate.failed_updates)

        response = self.client_empty(mac)
        self.assertEqual(status.HTTP_428_PRECONDITION_REQUIRED, response.status_code)
        self.assertEquals('Room is booked, but not canceling soon after start.', self.extract_msg(response))

        self.assertEquals(0, ReservationLog.objects.count())
        client.clientupdate.refresh_from_db()
        self.assertEquals(0, client.clientupdate.failed_updates)


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


class RegisterClientTest(TestCase):
    def setUp(self):
        self.client = Client()

    def client_register(self, mac, data=None):
        return self.client.post('/api/v1/clients/{}/register'.format(mac), data)

    def extract_error_msg(self, response):
        return json.loads(response.content.decode())['error']

    def extract_errors(self, response):
        return json.loads(response.content.decode())['errors']

    def extract_msg(self, response):
        return json.loads(response.content.decode())['message']

    def test_register_ok(self):
        mac = 'aa:bb:cc:dd:ee:ff'
        data = {
            'mac': mac,
            'ip': '127.0.0.1',
            'service_url': 'http://localhost:8001/api/v1',
        }
        response = self.client_register(mac, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEquals('Register client OK', self.extract_msg(response))
        self.assertEquals(1, DjinnClient.objects.count())

    def test_register_use_detected_ip(self):
        mac = 'aa:bb:cc:dd:ee:ff'
        data = {
            'mac': mac,
            'ip': '1.2.3.4',
            'service_url': 'http://localhost:8001/api/v1',
        }
        response = self.client_register(mac, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEquals('Register client OK', self.extract_msg(response))
        self.assertEquals(1, DjinnClient.objects.count())
        client = DjinnClient.objects.first()
        self.assertEquals('127.0.0.1', client.ip)
        self.assertEquals('http://127.0.0.1:8001/api/v1', client.service_url)

    def test_update_client(self):
        mac = 'aa:bb:cc:dd:ee:ff'
        orig_ip = 'x'
        DjinnClient.objects.create(mac=mac, ip=orig_ip)
        data = {
            'mac': mac,
            'service_url': 'http://localhost:8001/api/v1',
        }
        client = DjinnClient.objects.first()
        self.assertEquals(orig_ip, client.ip)

        response = self.client_register(mac, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEquals('Updated client', self.extract_msg(response))
        self.assertEquals(1, DjinnClient.objects.count())
        client = DjinnClient.objects.first()
        self.assertEquals('127.0.0.1', client.ip)

    def client_presence(self, mac):
        return self.client.put('/api/v1/clients/{}/presence'.format(mac))

    def client_empty(self, mac):
        return self.client.put('/api/v1/clients/{}/empty'.format(mac))

    def test_update_ip_on_presence(self):
        mac = 'aa:bb:cc:dd:ee:ff'
        orig_ip = 'x'
        DjinnClient.objects.create(mac=mac, ip=orig_ip)
        room = create_dummy_room()
        client = DjinnClient.objects.first()
        client.room = room
        client.save()
        self.assertEquals(orig_ip, client.ip)

        response = self.client_presence(mac)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        client = DjinnClient.objects.first()
        self.assertEquals('127.0.0.1', client.ip)

    def test_update_ip_on_empty(self):
        mac = 'aa:bb:cc:dd:ee:ff'
        orig_ip = 'x'
        DjinnClient.objects.create(mac=mac, ip=orig_ip)
        room = create_dummy_room()
        client = DjinnClient.objects.first()
        client.room = room
        client.save()
        self.assertEquals(orig_ip, client.ip)

        response = self.client_empty(mac)
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        client = DjinnClient.objects.first()
        self.assertEquals('127.0.0.1', client.ip)

    def test_register_two_clients_with_distinct_mac_but_same_ip_ok(self):
        mac1 = 'aa:bb:cc:dd:ee:ff'
        response = self.client_register(mac1, {'mac': mac1})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        mac2 = 'aa:bb:cc:dd:ee:00'
        response = self.client_register(mac2, {'mac': mac2})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEquals(2, DjinnClient.objects.count())


class RunCommandTest(TestCase):
    def test_exit_code_0(self):
        returncode, out, err = run_cmd('echo', 'hello')
        self.assertEquals(0, returncode)
        self.assertEquals('hello', out)
        self.assertEquals('', err)

    def test_exit_code_1(self):
        returncode, out, err = run_cmd('ls', 'nonexistent')
        self.assertEquals(1, returncode)
        self.assertEquals('', out)
        self.assertEquals('ls: nonexistent: No such file or directory', err)

    def test_list_reservations(self):
        result = list_reservations(timezone.now(), timezone.now(), Room())
        self.assertEquals({}, result)

    def test_parse_date(self):
        date = datetime(2015, 9, 25, 18, 59)
        datestr = '2015-09-25 18:59'
        self.assertEquals(date, parse_date(datestr))

    def test_parse_reservations(self):
        jsonstr = '''{"90A05013": [
         {
              "start": "2015-09-25 18:30",
              "end": "2015-09-25 19:00"
         },
         {
              "start": "2015-09-25 18:30",
              "end": "2015-09-25 18:59"
         }
         ]}
        '''
        expected = {
            "90A05013": [
                {
                    'start': datetime(2015, 9, 25, 18, 30),
                    'end': datetime(2015, 9, 25, 19, 0),
                },
                {
                    'start': datetime(2015, 9, 25, 18, 30),
                    'end': datetime(2015, 9, 25, 18, 59),
                },
            ]
        }
        result = parse_reservations(jsonstr)
        self.assertEquals(expected, result)


def create_reservations(*pairs):
    return [
        {
            'start': pair[0],
            'end': pair[1],
        } for pair in pairs
    ]


class MergeReservationsTest(TestCase):
    def setUp(self):
        self.room = create_dummy_room()
        self.example1_find_better_name = [
            {
                'start': datetime(2015, 9, 25, 18, 30),
                'end': datetime(2015, 9, 25, 19, 0),
            },
            {
                'start': datetime(2015, 9, 25, 18, 30),
                'end': datetime(2015, 9, 25, 18, 59),
            },
        ]

    def test_simply_add_incoming(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(1, self.room.reservationlog_set.count())

        log = self.room.reservationlog_set.first()
        self.assertEquals(ReservationLog.TYPE_CREATE, log.log_type)
        self.assertEquals(ReservationLog.TRIGGER_EXT, log.log_trigger)

    def test_simply_add_nothing(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        Reservation.objects.create(room=self.room, start=start, end=end)
        reservations = []
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(0, self.room.reservationlog_set.count())

    def test_add_incoming_overlaps(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        reservations = create_reservations((start, end), (start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(2, self.room.reservation_set.count())
        self.assertEquals(2, self.room.reservationlog_set.count())

        log = self.room.reservationlog_set.first()
        self.assertEquals(ReservationLog.TYPE_CREATE, log.log_type)
        self.assertEquals(ReservationLog.TRIGGER_EXT, log.log_trigger)

    def test_remerge(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        reservations = create_reservations((start, end), (start, end))
        merge_reservations(self.room, reservations)
        merge_reservations(self.room, reservations)
        self.assertEquals(2, self.room.reservation_set.count())
        self.assertEquals(2, self.room.reservationlog_set.count())

        log = self.room.reservationlog_set.first()
        self.assertEquals(ReservationLog.TYPE_CREATE, log.log_type)
        self.assertEquals(ReservationLog.TRIGGER_EXT, log.log_trigger)

    def test_keep_exact_match(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        Reservation.objects.create(room=self.room, start=start, end=end)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(0, self.room.reservationlog_set.count())

    def test_keep_reservation_before(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        before_start = start - timedelta(minutes=60)
        Reservation.objects.create(room=self.room, start=before_start, end=start)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(2, self.room.reservation_set.count())
        self.assertEquals(1, self.room.reservationlog_set.count())

        log = self.room.reservationlog_set.first()
        self.assertEquals(ReservationLog.TYPE_CREATE, log.log_type)
        self.assertEquals(ReservationLog.TRIGGER_EXT, log.log_trigger)

    def test_keep_reservation_after(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        after_end = end + timedelta(minutes=60)
        Reservation.objects.create(room=self.room, start=end, end=after_end)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(2, self.room.reservation_set.count())
        self.assertEquals(1, self.room.reservationlog_set.count())

        log = self.room.reservationlog_set.first()
        self.assertEquals(ReservationLog.TYPE_CREATE, log.log_type)
        self.assertEquals(ReservationLog.TRIGGER_EXT, log.log_trigger)

    def test_remove_overlapping_at_start(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        before_start = start - timedelta(minutes=5)
        after_start = start + timedelta(minutes=5)
        Reservation.objects.create(room=self.room, start=before_start, end=after_start)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(2, self.room.reservationlog_set.count())

        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CANCEL,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )
        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CREATE,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )

    def test_remove_overlapping_at_end(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        before_end = end - timedelta(minutes=5)
        after_end = end + timedelta(minutes=5)
        Reservation.objects.create(room=self.room, start=before_end, end=after_end)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(2, self.room.reservationlog_set.count())

        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CANCEL,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )
        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CREATE,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )

    def test_remove_subset(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        after_start = start + timedelta(minutes=5)
        before_end = end - timedelta(minutes=5)
        Reservation.objects.create(room=self.room, start=after_start, end=before_end)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(2, self.room.reservationlog_set.count())

        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CANCEL,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )
        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CREATE,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )

    def test_remove_superset(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        before_start = start - timedelta(minutes=5)
        after_end = end + timedelta(minutes=5)
        Reservation.objects.create(room=self.room, start=before_start, end=after_end)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(2, self.room.reservationlog_set.count())

        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CANCEL,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )
        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CREATE,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )

    def test_remove_many(self):
        start = datetime(2015, 9, 25, 18, 30)
        end = datetime(2015, 9, 25, 19, 0)
        before_start = start - timedelta(minutes=5)
        before_end = end - timedelta(minutes=5)
        after_end = end + timedelta(minutes=5)
        Reservation.objects.create(room=self.room, start=before_start, end=before_end)
        Reservation.objects.create(room=self.room, start=before_end, end=after_end)
        Reservation.objects.create(room=self.room, start=start, end=before_end)
        reservations = create_reservations((start, end))
        merge_reservations(self.room, reservations)
        self.assertEquals(1, self.room.reservation_set.count())
        self.assertEquals(4, self.room.reservationlog_set.count())

        self.assertEquals(
            3, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CANCEL,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )
        self.assertEquals(
            1, ReservationLog.objects.filter(
                log_type=ReservationLog.TYPE_CREATE,
                log_trigger=ReservationLog.TRIGGER_EXT).count()
        )
