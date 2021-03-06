from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'rooms/(?P<room_id>[^/.]+)/reservations', views.RoomReservationViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'equipments', views.EquipmentViewSet)
router.register(r'find/rooms', views.FindRoomsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'find/rooms', views.find_rooms),
    url(r'clients/(?P<mac>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))/presence', views.client_presence),
    url(r'clients/(?P<mac>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))/empty', views.client_empty),
    url(r'clients/(?P<mac>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))/register', views.client_register),
    url(r'clients/(?P<mac>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))/heartbeat', views.client_heartbeat),
]
