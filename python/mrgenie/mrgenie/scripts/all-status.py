from datetime import datetime

from mrgenie.parsecom.services import ParseService
from mrgenie.utils import status


service = ParseService()
date = datetime.now()

for room in service.get_rooms():
    room_id = room[0]
    reservations = service.get_reservations(room_id)
    print('id: {} status: {}'.format(room_id, status.get_status(reservations, date)))
