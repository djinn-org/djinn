import json

import httplib2
import settings

# connection = httplib2.Http('api.parse.com', 443)
# resp, content = connection.request(
#     'https://api.parse.com/1/classes/Host',
#     'GET',
#     headers={
#         "X-Parse-Application-Id": settings.PARSE_APP_ID,
#         "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
#     }
# )
from mrgenie import services

# [('Ay4Qe3A1lC', 'A77-14J17'), ('eLSxvYeY9R', 'A77-12E50'), ('eU9npkV8mZ', 'A77-16J89')]
print(services.get_rooms())
reservations = services.get_reservations('Ay4Qe3A1lC')

print([x['start_date'] for x in reservations])
# print(json.dumps(reservations, indent=4))
