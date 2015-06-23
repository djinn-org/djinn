from datetime import datetime
from datetime import timedelta

STATUS_FREE = 'FREE'
STATUS_RESERVED = 'RESERVED'
STATUS_MEETING = 'MEETING'


def from_minutes(minutes):
    return timedelta(minutes=minutes)

PENDING_RESERVATION_TIMEDELTA = from_minutes(15)


def to_date_today(remote_date):
    today = datetime.now()
    return datetime(today.year, today.month, today.day,
                    remote_date.hour, remote_date.minute, remote_date.second)


def get_reservations(service, room_id):
    reservations = service.get_reservations(room_id)

    reservations_today = [
        {
            'start_date': to_date_today(x['start_date']),
            'end_date': to_date_today(x['end_date'])
        } for x in reservations]

    reservations_sorted = sorted(reservations_today, key=lambda x: x['start_date'])

    return reservations_sorted


def get_status(raw_reservations, time):
    reservations = get_relevant_reservations(get_clean_reservations(raw_reservations), time)
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
