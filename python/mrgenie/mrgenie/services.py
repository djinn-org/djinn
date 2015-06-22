import json
import datetime

from mrgenie import parsecom


def get_rooms():
    """
    Get all the rooms in the system
    :return: list of (id, name) tuples
    """
    rooms_json = json.loads(parsecom.get(path='/1/classes/Room').decode())
    rooms = rooms_json['results']
    return [(x['objectId'], x['name']) for x in rooms]


def get_all_reservations():
    reservations_json = json.loads(parsecom.get(path='/1/classes/Reservation').decode())
    reservations = reservations_json['results']
    return reservations


def to_date(strdate):
    return datetime.datetime.strptime(strdate[:19], "%Y-%m-%dT%H:%M:%S")


def get_reservations(room_id):
    reservations_json = json.loads(parsecom.get(
        path='/1/classes/Reservation',
        where={
            'room': {
                '__type': 'Pointer',
                'className': 'Room',
                'objectId': room_id
            }
        }
    ).decode())

    reservations = reservations_json['results']

    reservations_simple = [
        {
            'start_date': to_date(x['start_date']['iso']),
            'end_date': to_date(x['end_date']['iso'])
        } for x in reservations]

    reservations_sorted = sorted(reservations_simple, key=lambda x: x['start_date'])

    return reservations_sorted
