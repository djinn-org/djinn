from datetime import datetime
from datetime import timedelta
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


def to_parse_date(date):
    return {
        "__type": "Date",
        "iso": date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }


class ParseService(Service):
    def get_rooms(self):
        rooms_json = json.loads(get(path='/1/classes/Room').decode())
        rooms = rooms_json['results']
        return [(x['objectId'], x['name']) for x in rooms]

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

    def make_reservation(self, room_id):
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
                    "objects": [{
                        "__type": "Pointer",
                        "className": "Room",
                        "objectId": room_id
                    }]
                }
            }

            put(path=reservation_path, params=rel_params)

        return resp

    def cancel_reservation(self, room_id):
        pass


def to_date(strdate):
    return datetime.strptime(strdate[:19], "%Y-%m-%dT%H:%M:%S")
