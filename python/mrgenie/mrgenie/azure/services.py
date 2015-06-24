from datetime import datetime
import json

import httplib2
from mrgenie.services import Service

BASEURL = 'https://testinnovathon.azurewebsites.net'
BASEURL = 'http://192.168.206.211:4017'
# http://192.168.206.211:4017/api/booking?roomname=R1.1&status=Cancel
# http://192.168.206.211:4017/api/booking?roomname=R1.1&status=Book


def get(path, params=''):
    http = httplib2.Http('.cache', 443)
    resp, content = http.request(
        BASEURL + path + '?' + params,
        'GET'
    )
    return json.loads(content.decode())


class AzureService(Service):
    def get_rooms(self):
        rooms = get(path='/api/room')
        return [(x['Name'].strip(), x['Name'].strip()) for x in rooms]

    def get_reservations(self, room_id):
        reservations_raw = get(
            path='/api/reservation',
            params='roomName={}'.format(room_id)
        )

        reservations = [
            {
                'start_date': to_date(x['Start']),
                'end_date': to_date(x['Fin'])
            } for x in reservations_raw]

        return reservations

    def make_reservation(self, room_id):
        resp = get(path='/api/booking', params='roomname={}&status=Book'.format(room_id))
        return resp['Status'] == 'OK'

    def cancel_reservation(self, room_id):
        resp = get(path='/api/booking', params='roomname={}&status=Cancel'.format(room_id))
        return resp['Status'] == 'OK' and resp['Id'] == 1


def to_date(strdate):
    return datetime.strptime(strdate[:19], "%Y-%m-%dT%H:%M:%S")


