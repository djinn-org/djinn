from datetime import datetime
import sys

from mrgenie.parsecom.services import ParseService
from mrgenie.utils import status


room_id = sys.argv[1]

service = ParseService()

date = datetime.now()
reservations = service.get_reservations(room_id)
print(status.get_status(reservations, date))
