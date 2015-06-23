from datetime import datetime
import json

import httplib2
from mrgenie.services import Service
import settings


def get(path, params=''):
    http = httplib2.Http('.cache', 443)
    resp, content = http.request(
        'https://api.parse.com/{}'.format(path) + '?' + params,
        'GET',
        headers={
            "X-Parse-Application-Id": settings.PARSE_APP_ID,
            "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
        }
    )
    return content


class ParseService(Service):
    def get_rooms(self):
        rooms_json = json.loads(get(path='/1/classes/Room').decode())
        rooms = rooms_json['results']
        return [(x['objectId'], x['name']) for x in rooms]

    def get_all_reservations(self):
        reservations_json = json.loads(get(path='/1/classes/Reservation').decode())
        reservations = reservations_json['results']
        return reservations

    def get_reservations(self, room_id):
        reservations_json = json.loads(get(
            path='/1/classes/Reservation',
            params='where={"room":{"__type":"Pointer","className":"Room","objectId":"%s"}}' % room_id
        ).decode())

        reservations_raw = reservations_json['results']

        reservations = [
            {
                'start_date': to_date(x['start_date']['iso']),
                'end_date': to_date(x['end_date']['iso'])
            } for x in reservations_raw]

        return reservations


def to_date(strdate):
    return datetime.strptime(strdate[:19], "%Y-%m-%dT%H:%M:%S")


