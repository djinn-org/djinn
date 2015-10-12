from django.core.management.base import BaseCommand
from djinn.models import ReservationLog
from django.utils.timezone import datetime, timedelta


def format_time(dt):
    return dt.strftime('%H:%m')


class Command(BaseCommand):
    help = 'Show reservation log stats'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--room', )
        parser.add_argument('--time-saved', )
        parser.add_argument('--day', )

    def msg(self, message):
        self.stdout.write('* ' + message)

    def print_saved_time(self, qs):
        cancel_djinn_list = qs.filter(
            log_type=ReservationLog.TYPE_CANCEL,
            log_trigger=ReservationLog.TRIGGER_DJINN
        ).order_by('room', 'log_time')

        total_time_saved = 0

        for cancel_djinn in cancel_djinn_list:
            create_ext_list = qs.filter(
                room=cancel_djinn.room,
                log_type=ReservationLog.TYPE_CREATE,
                log_trigger=ReservationLog.TRIGGER_EXT,
                start=cancel_djinn.start, end=cancel_djinn.end,
                log_time__lt=cancel_djinn.log_time
            )[:1]

            for create_ext in create_ext_list:
                saved = (create_ext.end - cancel_djinn.log_time).seconds // 60
                self.stdout.write('{} {} {:%H:%M} {} canceled at {:%H:%M:%S} {}'.format(
                    saved, create_ext.room.external_name,
                    create_ext.start, create_ext.minutes, cancel_djinn.log_time,
                    cancel_djinn.pk))

                total_time_saved += saved

        self.stdout.write("---")
        self.stdout.write("total time saved = {}".format(total_time_saved))

    def handle(self, *args, **options):
        qs = ReservationLog.objects

        if options['room']:
            qs = qs.filter(room__external_name=options['room'])
        if options['day']:
            day = datetime.strptime(options['day'], '%Y-%m-%d')
            qs = qs.filter(start__gte=day, end__lt=day + timedelta(days=1))

        self.print_saved_time(qs)
