from django.contrib import admin

from .models import Room
from .models import Equipment
from .models import RoomEquipment
from .models import Reservation

admin.site.register(Room)
admin.site.register(Equipment)
admin.site.register(RoomEquipment)
admin.site.register(Reservation)
