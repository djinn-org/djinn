from datetime import datetime
import json

import httplib2
from mrgenie.services import Service


def get(path, params=''):
    http = httplib2.Http('.cache', 443)
    resp, content = http.request(
        'https://testinnovathon.azurewebsites.net' + path + '?' + params,
        'GET'
    )
    return content


class AzureService(Service):
    def get_rooms(self):
        rooms = json.loads(get(path='/api/room').decode())
        return [(x['Name'].strip(), x['Name'].strip()) for x in rooms]

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


