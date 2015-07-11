from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=20)
    building = models.CharField(max_length=20)
    floor = models.IntegerField()
    number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


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
    room = models.ForeignKey(Room)
    start = models.DateTimeField()
    end = models.DateTimeField()
