from datetime import timedelta

from django import forms
from django_djinn_backend import settings
import re
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Building(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Room(models.Model):
    building = models.ForeignKey(Building)
    floor = models.IntegerField()
    name = models.CharField(max_length=20)
    external_name = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('building', 'floor', 'name'),)
        ordering = ('external_name',)

    def is_available(self):
        now = timezone.now()
        start = now + settings.WAIT_DELTA
        return not Reservation.objects.filter(room=self, start__lte=start, end__gt=now).exists()

    def calc_minutes_to_next_reservation(self):
        now = timezone.now()
        next_reservation = Reservation.objects.filter(room=self, start__gte=now).order_by('start').first()
        if next_reservation:
            return (next_reservation.start - now).seconds // 60
        return settings.AUTO_RESERVATION_MINUTES

    def get_current_reservation(self):
        now = timezone.now()
        return Reservation.objects.filter(room=self, start__lte=now, end__gt=now).order_by('start').first()

    @property
    def status(self):
        # TODO: +WAITING
        return 'FREE' if self.is_available() else 'OCCUPIED'


class Equipment(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class RoomEquipment(models.Model):
    room = models.ForeignKey(Room)
    equipment = models.ForeignKey(Equipment)

    def __str__(self):
        return '{} - {}'.format(self.room, self.equipment)

    class Meta:
        unique_together = (('room', 'equipment'),)


class IllegalReservation(Exception):
    pass


class Reservation(models.Model):
    user = models.ForeignKey(User, null=True)
    room = models.ForeignKey(Room)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True)
    minutes = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        if self.minutes and not self.end:
            self.end = self.start + timedelta(minutes=self.minutes)
        if not self.minutes and self.end:
            self.minutes = (self.end - self.start).seconds // 60
        '''
        if Reservation.objects.filter(room=self.room, start__lt=self.start, end__gt=self.start).exists():
            raise IllegalReservation()
        if Reservation.objects.filter(room=self.room, start__lt=self.end, end__gt=self.end).exists():
            raise IllegalReservation()
        if Reservation.objects.filter(room=self.room, start__gt=self.start, end__lte=self.end).exists():
            raise IllegalReservation()
        if Reservation.objects.filter(room=self.room, start__gte=self.start, end__lt=self.end).exists():
            raise IllegalReservation()
        '''
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.start, self.end)

    class Meta:
        ordering = ('room', 'start', 'minutes',)


def make_choices(*values):
    return [(value, value.title()) for value in values]


class ReservationLog(models.Model):
    TYPE_CREATE = 'create'
    TYPE_CANCEL = 'cancel'

    TRIGGER_DJINN = 'djinn'
    TRIGGER_APP = 'app'
    TRIGGER_WEB = 'web'
    TRIGGER_EXT = 'ext'

    reservation_pk = models.IntegerField()
    user = models.ForeignKey(User, null=True)
    room = models.ForeignKey(Room)
    start = models.DateTimeField()
    end = models.DateTimeField()
    minutes = models.IntegerField()

    log_type = models.CharField(max_length=50, choices=make_choices(TYPE_CREATE, TYPE_CANCEL))
    log_trigger = models.CharField(max_length=50, choices=make_choices(
        TRIGGER_DJINN, TRIGGER_APP, TRIGGER_WEB, TRIGGER_EXT))
    log_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ', '.join([str(x) for x in [self.user, self.room, self.start, self.minutes, self.log_type, self.log_trigger]])

    class Meta:
        ordering = ('-log_time',)
        # unique_together = (('reservation_pk', 'log_type'),)

    @staticmethod
    def create_from_reservation(reservation, log_type, log_trigger):
        ReservationLog.objects.create(reservation_pk=reservation.pk,
                                      user=reservation.user, room=reservation.room,
                                      start=reservation.start, end=reservation.end, minutes=reservation.minutes,
                                      log_type=log_type, log_trigger=log_trigger)


mac_re = re.compile(r'^([0-9a-fA-F]{2}([:-]|$)){6}$')


class MACAddressFormField(forms.RegexField):
    default_error_messages = {
        'invalid': _(u'Enter a valid MAC address.'),
    }

    def __init__(self, *args, **kwargs):
        super(MACAddressFormField, self).__init__(mac_re, *args, **kwargs)


class MACAddressField(models.Field):
    empty_strings_allowed = False
    description = _("MAC address")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 17
        super(MACAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': MACAddressFormField,
        }
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)


class Client(models.Model):
    ip = models.GenericIPAddressField()
    mac = MACAddressField(unique=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
    room = models.OneToOneField(Room, null=True, blank=True)
    service_url = models.URLField()
    enabled = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, **kwargs):
        is_new = self.id is None
        super(Client, self).save(force_insert, force_update)
        if is_new:
            ClientHeartbeat.objects.create(client=self)
            ClientUpdate.objects.create(client=self)

    def __str__(self):
        return self.alias or self.ip

    class Meta:
        ordering = ('mac',)

    def is_alive(self):
        return False

    def received_heartbeat(self):
        self.clientheartbeat.save()

    def increment_failed_updates(self):
        self.clientupdate.failed_updates += 1
        self.clientupdate.save()

    def clear_failed_updates(self):
        self.clientupdate.failed_updates = 0
        self.clientupdate.save()

    def update_status(self, status):
        # TODO: REST call to self.service_url
        self.increment_failed_updates()


class ClientHeartbeat(models.Model):
    client = models.OneToOneField(Client)
    last_heartbeat = models.DateTimeField(auto_now=True)


class ClientUpdate(models.Model):
    client = models.OneToOneField(Client)
    failed_updates = models.IntegerField(default=0)
