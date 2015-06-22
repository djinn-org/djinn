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


STATUS_FREE = 'FREE'
STATUS_RESERVED = 'RESERVED'
STATUS_MEETING = 'MEETING'


def from_minutes(minutes):
    return datetime.timedelta(seconds=minutes * 60)

PENDING_RESERVATION_TIMEDELTA = from_minutes(15)


def get_status(reservations0, time):
    reservations = get_relevant_reservations(get_clean_reservations(reservations0), time)
    timeline = []
    for i, reservation in enumerate(reservations):
        pending_date = reservation['start_date'] - PENDING_RESERVATION_TIMEDELTA
        timeline.append({'status': STATUS_RESERVED, 'time': pending_date})
        timeline.append({'status': STATUS_MEETING, 'time': reservation['start_date']})

        if i + 1 < len(reservations):
            next_reservation = reservations[i + 1]
            next_pending_date = next_reservation['start_date'] - PENDING_RESERVATION_TIMEDELTA
            if reservation['end_date'] < next_pending_date:
                timeline.append({'status': STATUS_FREE, 'time': reservation['end_date']})

    status = STATUS_FREE

    for entry in timeline:
        if time < entry['time']:
            return status
        status = entry['status']

    return status


def get_clean_reservations(reservations):
    return [item for item in reservations
            if item['start_date'] and item['end_date'] and item['end_date'] > item['start_date']]


def get_relevant_reservations(reservations, time):
    return [item for item in reservations
            if item['end_date'] > time >= item['start_date'] - PENDING_RESERVATION_TIMEDELTA]
