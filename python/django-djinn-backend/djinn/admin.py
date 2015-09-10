from django.contrib import admin

from .models import Building
from .models import Room
from .models import Equipment
from .models import RoomEquipment
from .models import Reservation


class RoomEquipmentInline(admin.StackedInline):
    model = RoomEquipment
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomEquipmentInline]


admin.site.register(Building)
admin.site.register(Room, RoomAdmin)
admin.site.register(Equipment)
admin.site.register(RoomEquipment)
admin.site.register(Reservation)
