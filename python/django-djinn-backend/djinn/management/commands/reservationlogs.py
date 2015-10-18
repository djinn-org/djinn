from django.core.management.base import BaseCommand
from djinn.models import ReservationLog, Reservation, Room
from django.utils.timezone import datetime, timedelta


def format_time(dt):
    return dt.strftime('%H:%m')


class Command(BaseCommand):
    help = 'Show reservation log stats'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['time-saved', 'fix-cancel-links', 'fix-reservation-pk'])
        parser.add_argument('--room', '-r')
        parser.add_argument('--day', '-d')

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

    def print_booking_count(self, qs):
        def count_rooms_booked_by(trigger):
            return qs.filter(
                log_type=ReservationLog.TYPE_CREATE,
                log_trigger=trigger
            ).count()
        booked_by_ext = count_rooms_booked_by(ReservationLog.TRIGGER_EXT)
        booked_by_djinn = count_rooms_booked_by(ReservationLog.TRIGGER_DJINN)

        self.stdout.write("---")
        self.stdout.write("rooms booked by ext = {}".format(booked_by_ext))
        self.stdout.write("rooms booked by djinn = {}".format(booked_by_djinn))

    def fix_reservation_pk(self, qs):
        create_list = qs.filter(
            log_type=ReservationLog.TYPE_CREATE,
            reservation_pk=0
        ).order_by('room', 'log_time')

        room = Room.objects.first()
        start = datetime(2015, 9, 15, 10, 0)

        for create_item in create_list:
            fake_reservation = Reservation.objects.create(room=room, start=start, minutes=1)
            pk = fake_reservation.pk
            fake_reservation.delete()
            self.stdout.write('setting unused reservation_pk = {} for {}'.format(pk, create_item))

            # NOTE: cannot do this way, it will update log_time
            # create_item.save()
            create_list.filter(pk=create_item.pk).update(
                log_time=create_item.log_time,
                reservation_pk=pk
            )

    def fix_cancel_links(self, qs):
        cancel_list = qs.filter(
            log_type=ReservationLog.TYPE_CANCEL,
            reservation_pk=0
        ).order_by('room', 'log_time')

        for cancel_item in cancel_list:
            create_list = qs.filter(
                room=cancel_item.room,
                log_type=ReservationLog.TYPE_CREATE,
                start=cancel_item.start, end=cancel_item.end,
                log_time__lt=cancel_item.log_time
            )

            print('cancel item:\n  {}'.format(cancel_item))

            if create_list:
                print('will link to:\n  {}'.format(create_list[0]))
                # NOTE: cannot do this way, it will update log_time
                # cancel_item.save()
                cancel_list.filter(pk=cancel_item.pk).update(
                    log_time=cancel_item.log_time,
                    reservation_pk=create_list[0].reservation_pk
                )

                for create_item in create_list[1:]:
                    print('will NOT link to:\n  {}'.format(create_item))

            else:
                print('no matching create logs for {}'.format(cancel_item))

            print()

    def handle(self, *args, **options):
        qs = ReservationLog.objects

        if options['room']:
            qs = qs.filter(room__external_name=options['room'])
        if options['day']:
            day = datetime.strptime(options['day'], '%Y-%m-%d')
            qs = qs.filter(start__gte=day, end__lt=day + timedelta(days=1))

        action = options['action']
        if action == 'fix-cancel-links':
            self.fix_cancel_links(qs)
        elif action == 'fix-reservation-pk':
            self.fix_reservation_pk(qs)
        elif action == 'time-saved':
            self.print_saved_time(qs)
            self.print_booking_count(qs)
