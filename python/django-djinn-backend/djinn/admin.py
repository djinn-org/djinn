from django.contrib import admin

from .models import Building, Client
from .models import Room
from .models import Equipment
from .models import RoomEquipment
from .models import Reservation
from .models import ReservationLog


class RoomEquipmentInline(admin.StackedInline):
    model = RoomEquipment
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomEquipmentInline]


class EquipmentAdmin(admin.ModelAdmin):
    inlines = [RoomEquipmentInline]


class ReservationLogAdmin(admin.ModelAdmin):
    model = ReservationLog
    list_display = ('user', 'room', 'start', 'end', 'log_type', 'log_trigger')

class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('ip', 'mac', 'alias', 'room', 'is_alive', 'get_last_heartbeat')

    def get_last_heartbeat(self, client):
        return client.clientheartbeat.last_heartbeat
    get_last_heartbeat.short_description = 'Last heartbeat'

admin.site.register(Building)
admin.site.register(Room, RoomAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(RoomEquipment)
admin.site.register(Reservation)
admin.site.register(ReservationLog, ReservationLogAdmin)
admin.site.register(Client, ClientAdmin)
