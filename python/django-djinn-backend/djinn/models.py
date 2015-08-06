from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Room(models.Model):
    building = models.ForeignKey(Building)
    floor = models.IntegerField()
    name = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return '{}-{}F.{}'.format(self.building, self.floor, self.name)

    class Meta:
        unique_together = (('building', 'floor', 'name'),)


class Equipment(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class RoomEquipment(models.Model):
    room = models.ForeignKey(Room)
    equipment = models.ForeignKey(Equipment)

    def __str__(self):
        return '{} - {}'.format(self.room, self.equipment)


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
