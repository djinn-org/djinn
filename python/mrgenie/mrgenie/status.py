from datetime import datetime
from mrgenie import services
import sys

room_id = sys.argv[1]

date = datetime.now()
reservations = services.get_reservations(room_id)
print(services.get_status(reservations, date))
