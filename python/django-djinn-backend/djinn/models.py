from datetime import timedelta

from django import forms
import re
from django.contrib.auth.models import User
from django.core import validators, checks
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Building(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    building = models.ForeignKey(Building)
    floor = models.IntegerField()
    name = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return '{}-{}.{}'.format(self.building, self.floor, self.name)

    class Meta:
        unique_together = (('building', 'floor', 'name'),)


class Equipment(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


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
        if Reservation.objects.filter(room=self.room, end__gt=self.start, end__lt=self.end).exists():
            raise IllegalReservation()
        if Reservation.objects.filter(room=self.room, start__gt=self.start, start__lt=self.end).exists():
            raise IllegalReservation()
        if Reservation.objects.filter(room=self.room, start__gt=self.start, end__lt=self.end).exists():
            raise IllegalReservation()
        if Reservation.objects.filter(room=self.room, start__lt=self.start, end__gt=self.end).exists():
            raise IllegalReservation()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.start, self.end)


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
    ip = models.GenericIPAddressField(unique=True)
    mac = MACAddressField(unique=True)
    alias = models.TextField(unique=True, null=True)
    room = models.ForeignKey(Room, unique=True, null=True)
    service_url = models.URLField(unique=True)

    def save(self, force_insert=False, force_update=False, **kwargs):
        is_new = self.id is None
        super(Client, self).save(force_insert, force_update)
        if is_new:
            ClientHeartbeat.objects.create(client=self)
            ClientUpdate.objects.create(client=self)

    def is_alive(self):
        return False

    def received_heartbeat(self):
        try:
            heartbeat = self.clientheartbeat
        except ClientHeartbeat.DoesNotExist:
            heartbeat = ClientHeartbeat(client=self)
        heartbeat.last_heartbeat = timezone.now()
        heartbeat.save()

    def increment_failed_updates(self):
        pass

    def clear_failed_updates(self):
        pass

    def __str__(self):
        return self.alias or self.ip


class ClientHeartbeat(models.Model):
    client = models.OneToOneField(Client)
    last_heartbeat = models.DateTimeField(auto_now=True)


class ClientUpdate(models.Model):
    client = models.OneToOneField(Client)
    failed_updates = models.IntegerField(default=0)
