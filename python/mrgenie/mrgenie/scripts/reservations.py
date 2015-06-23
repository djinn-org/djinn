import sys
from mrgenie.parsecom.services import ParseService

room_id = sys.argv[1]

service = ParseService()

for reservation in service.get_reservations(room_id):
    print(reservation)
