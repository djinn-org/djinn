from mrgenie import services

for room in services.get_rooms():
    print('id: {} name: {}'.format(*room))
