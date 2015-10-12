from django.core.management.base import BaseCommand
from djinn.models import ReservationLog
from django.utils.timezone import datetime, timedelta


def format_time(datetime):
    return datetime.strftime('%H:%m')


class Command(BaseCommand):
    help = 'Show reservation log stats'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--room', )
        parser.add_argument('--time-saved', )
        parser.add_argument('--day', )

    def msg(self, message):
        self.stdout.write('* ' + message)

    def handle(self, *args, **options):
        qs = ReservationLog.objects
        if options['room']:
            qs = qs.filter(room__external_name=options['room'])
        if options['day']:
            day = datetime.strptime(options['day'], '%Y-%m-%d')
            qs = qs.filter(start__gte=day, end__lt=day + timedelta(days=1))

        cancel_djinn_list = qs.filter(
            log_type=ReservationLog.TYPE_CANCEL,
            log_trigger=ReservationLog.TRIGGER_DJINN).order_by('room', 'log_time')

        for cancel_djinn in cancel_djinn_list:
            create_ext_list = qs.filter(
                room=cancel_djinn.room, log_type=ReservationLog.TYPE_CREATE,
                log_trigger=ReservationLog.TRIGGER_EXT, start=cancel_djinn.start,
                end=cancel_djinn.end)

            for create_ext in create_ext_list:
                saved = (create_ext.end - cancel_djinn.log_time).seconds // 60
                print('{} {} {:%H:%m} {} canceled at {:%H:%m:%S} {}'.format(
                    saved, create_ext.room, create_ext.start, create_ext.minutes, cancel_djinn.log_time,
                    cancel_djinn.pk))
