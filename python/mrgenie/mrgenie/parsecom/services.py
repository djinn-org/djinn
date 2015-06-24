from datetime import datetime
from datetime import timedelta
import json

import httplib2
from mrgenie.services import Service
import settings


def urlencode(params):
    return '&'.join(['{}={}'.format(k, json.dumps(v).replace(' ', ''))
                     for k, v in params.items()])


def get(path, params=None):
    if not params:
        params = {}

    params_urlencoded = urlencode(params)
    http = httplib2.Http('.cache', 443)
    resp, content = http.request(
        'https://api.parse.com/{}?{}'.format(path, params_urlencoded),
        'GET',
        headers={
            "X-Parse-Application-Id": settings.PARSE_APP_ID,
            "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
        }
    )
    return content.decode()


def post_or_put(path, params=None, method='POST'):
    if not params:
        params = {}

    http = httplib2.Http('.cache', 443)
    resp, content = http.request(
        'https://api.parse.com/' + path,
        method,
        headers={
            "X-Parse-Application-Id": settings.PARSE_APP_ID,
            "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
        },
        body=json.dumps(params)
    )
    return content.decode()


def post(path, params=None):
    return post_or_put(path, params)


def put(path, params=None):
    return post_or_put(path, params, method='PUT')


def delete(path):
    http = httplib2.Http('.cache', 443)
    resp, content = http.request(
        'https://api.parse.com/' + path,
        'DELETE',
        headers={
            "X-Parse-Application-Id": settings.PARSE_APP_ID,
            "X-Parse-REST-API-Key": settings.PARSE_REST_KEY
        }
    )
    return content.decode()


def to_parse_date(date):
    return {
        "__type": "Date",
        "iso": date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }


class ParseService(Service):
    def get_rooms(self):
        rooms_json = json.loads(get(path='/1/classes/Room'))
        rooms = rooms_json['results']
        return [(x['objectId'], x['name']) for x in rooms]

    def get_reservations(self, room_id):
        path = '/1/classes/Reservation'
        params = {
            'where': {
                'room': {
                    '__type': 'Pointer',
                    'className': 'Room',
                    'objectId': room_id
                }
            }
        }

        reservations_raw = json.loads(get(path, params))['results']

        reservations = [
            {
                'start_date': to_date(x['start_date']['iso']),
                'end_date': to_date(x['end_date']['iso']),
                'objectId': x['objectId'],
            } for x in reservations_raw]

        return reservations

    def get_current_reservation_id(self, room_id):
        start_date = datetime.now()
        reservations = self.get_reservations(room_id)
        for reservation in reservations:
            if reservation['start_date'] < start_date < reservation['end_date']:
                return reservation['objectId']

    def make_reservation(self, room_id):
        if self.get_current_reservation_id(room_id):
            return False

        start_date = datetime.now()
        end_date = start_date + timedelta(minutes=30)
        params = {
            'start_date': to_parse_date(start_date),
            'end_date': to_parse_date(end_date)
        }

        path = '/1/classes/Reservation'
        resp = post(path=path, params=params)
        if resp:
            reservation_object_id = json.loads(resp)['objectId']
            reservation_path = path + '/' + reservation_object_id
            rel_params = {
                'room': {
                    "__op": "AddRelation",
                    "objects": [
                        {
                            "__type": "Pointer",
                            "className": "Room",
                            "objectId": room_id
                        }
                    ]
                }
            }

            put(path=reservation_path, params=rel_params)

        return resp

    def cancel_reservation(self, room_id):
        reservation_id = self.get_current_reservation_id(room_id)
        if reservation_id:
            delete('/1/classes/Reservation/' + reservation_id)
            return True
        return False


def to_date(strdate):
    return datetime.strptime(strdate[:19], "%Y-%m-%dT%H:%M:%S")
