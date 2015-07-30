from django.test import TestCase
from django.test import Client
from djinn.models import Room, Building, Equipment


class SearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.building = Building.objects.create(name='main')

        self.room1_data = {
            'building': self.building,
            'floor': 12,
            'name': 'E50',
            'capacity': 8,
        }
        Room.objects.create(**self.room1_data)

        self.room2_data = {
            'building': self.building,
            'floor': 16,
            'name': 'J89',
            'capacity': 20,
        }
        Room.objects.create(**self.room2_data)

    def test_list_rooms(self):
        response = self.client.get('/api/v1/rooms/')
        self.assertEqual(response.status_code, 200)

        json = response.content.decode()
        self.assertJSONEqual(json, [{
            'id': 1,
            'building': self.building.pk,
            'floor': 12,
            'name': 'E50',
            'capacity': 8,
        }, {
            'id': 2,
            'building': self.building.pk,
            'floor': 16,
            'name': 'J89',
            'capacity': 20,
        }])

    # def test_list_equipment(self):
    #     self.assertEqual(1, 1)

# verify json responses
# get list of rooms
# search by criteria
#   calculate rank: match on capacity, match on equipment, match on availability
# get list of possible equipments


class EquipmentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.pc = Equipment.objects.create(name="PC")
        self.phone = Equipment.objects.create(name="Phone")

    def test_list_equipment(self):
        response = self.client.get('/api/v1/equipments/')
        self.assertEqual(response.status_code, 200)

        json = response.content.decode()
        self.assertJSONEqual(json, [{
            'id': 1,
            'name': 'PC',
        }, {
            'id': 2,
            'name': 'Phone',
        }])
