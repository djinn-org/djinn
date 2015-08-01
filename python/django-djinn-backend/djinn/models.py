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


class Equipment(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class RoomEquipment(models.Model):
    room = models.ForeignKey(Room)
    equipment = models.ForeignKey(Equipment)

    def __str__(self):
        return '{} - {}'.format(self.room, self.equipment)


class Reservation(models.Model):
    user = models.ForeignKey(User, null=True)
    room = models.ForeignKey(Room)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True)
    minutes = models.IntegerField(blank=True)
