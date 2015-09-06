import re
from django.core.management.base import BaseCommand, CommandError
from djinn.models import Room, Equipment, RoomEquipment, Building
from bs4 import BeautifulSoup
from collections import namedtuple

RESOURCE_TYPE_ROOM = 'ResourceType:Room'


class Command(BaseCommand):
    help = 'Show and manipulate rooms'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--list', action='store_true',
                            help='list rooms')
        parser.add_argument('--import', metavar='XMLFILE',
                            help='import rooms from XML dump')

    def do_list(self):
        for room in Room.objects.all():
            self.stdout.write(str(room))

    def do_import_path(self, path):
        with open(path) as fh:
            self.do_import_soup(BeautifulSoup(fh, 'html.parser'))

    def do_import_soup(self, soup):
        # later: update room
        # later: option to delete rooms that disappeared
        known_items = {item.name: item for item in Equipment.objects.all()}
        known_rooms = {str(room): room for room in Room.objects.all()}

        RoomData = namedtuple('RoomData', ['name', 'mail', 'capacity', 'items'])

        def parse_room_data(room_soup):
            room_type = room_soup.find('type').text
            if room_type != RESOURCE_TYPE_ROOM:
                return

            name = room_soup.find('name').text
            mail = room_soup.find('mail').text
            capacity = int(room_soup.find('capacity').text)
            items = room_soup.find('equipment').text.split(',')

            return RoomData(name, mail, capacity, items)

        def get_or_create_items(items_data):
            for name in items_data:
                if name in known_items:
                    yield known_items[name]
                else:
                    item = Equipment.objects.create(name=name)
                    known_items[name] = item
                    self.msg('new equipment: {}'.format(item))
                    yield item

        def get_or_create_building(name):
            return Building.objects.get_or_create(name=name)[0]

        def get_or_create_room(room_data):
            match = re.match(r'^(?P<building>.+)-(?P<floor>\d+)\.(?P<name>\w+)', room_data.name)
            building = get_or_create_building(match.group('building'))
            floor = int(match.group('floor'))
            name = match.group('name')
            capacity = room_data.capacity

            room = Room(building=building, floor=floor, name=name, capacity=capacity)

            room_str = str(room)
            if room_str in known_rooms:
                return known_rooms[room_str]

            room.save()
            known_rooms[room_str] = room
            self.msg('new room: ' + room_str)
            return room

        def register_room_items(room, items):
            for equipment in items:
                RoomEquipment.objects.get_or_create(room=room, equipment=equipment)

        for room_soup in soup.find_all('room'):
            room_data = parse_room_data(room_soup)
            if room_data:
                room = get_or_create_room(room_data)
                items = get_or_create_items(room_data.items)
                register_room_items(room, items)

    def msg(self, message):
        self.stdout.write('* ' + message)

    def handle(self, *args, **options):
        if options['list']:
            self.do_list()
        elif options['import']:
            self.do_import_path(options['import'])
