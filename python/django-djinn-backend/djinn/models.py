from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=20)
    building = models.CharField(max_length=20)
    floor = models.IntegerField()
    number = models.IntegerField()
    capacity = models.IntegerField()


class Equipment(models.Model):
    name = models.CharField(max_length=20)


class RoomEquipment(models.Model):
    room = models.ForeignKey(Room)
    equipment = models.ForeignKey(Equipment)
