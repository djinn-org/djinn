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
    # url(r'find/rooms', views.find_rooms),
]
