import re
from django.core.management.base import BaseCommand
from djinn.models import Room, Equipment, RoomEquipment, Building, ReservationLog
from bs4 import BeautifulSoup
from collections import namedtuple
from django.utils.timezone import datetime, timedelta


class Command(BaseCommand):
    help = 'Show reservation log stats'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--room',)
        parser.add_argument('--time-saved',)
        parser.add_argument('--day',)

    def msg(self, message):
        self.stdout.write('* ' + message)

    def handle(self, *args, **options):
        qs = ReservationLog.objects
        if options['room']:
            qs = qs.filter(room__external_name=options['room'])
        if options['day']:
            day = datetime.strptime(options['day'], '%Y-%m-%d')
            qs = qs.filter(start__gte=day, end__lt=day + timedelta(days=1))

        for log in qs.filter(log_type=ReservationLog.TYPE_CANCEL, log_trigger=ReservationLog.TRIGGER_DJINN):
            for orig in qs.filter(log_type=ReservationLog.TYPE_CREATE, log_trigger=ReservationLog.TRIGGER_EXT, start=log.start, end=log.end):
                print(orig)
