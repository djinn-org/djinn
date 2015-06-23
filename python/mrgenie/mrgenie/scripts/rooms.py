from mrgenie.parsecom.services import ParseService

service = ParseService()

for room in service.get_rooms():
    print('id: {} name: {}'.format(*room))
