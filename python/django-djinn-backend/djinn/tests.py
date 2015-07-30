from django.test import TestCase
from django.test import Client
from djinn.models import Room, Building, Equipment
from api.serializers import RoomSerializer, EquipmentSerializer


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

    # def test_list_equipment(self):
    #     self.assertEqual(1, 1)

# verify json responses
# get list of rooms
# search by criteria
#   calculate rank: match on capacity, match on equipment, match on availability
# get list of possible equipments


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
