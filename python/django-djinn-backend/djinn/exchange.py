from datetime import datetime, timedelta
import json
from subprocess import Popen, PIPE

from django_djinn_backend import settings


def ready():
    return settings.EXCHANGE_CONNECTOR_READY


def format_date_param(date):
    return date.strftime('%Y%m%d%H%M')


def parse_date(datestr):
    return datetime.strptime(datestr, '%Y-%m-%d %H:%M')


def parse_reservations(jsonstr):
    reservations = {}
    for roomname, values in json.loads(jsonstr).items():
        reservations[roomname] = [{
            'start': parse_date(value['start']),
            'end': parse_date(value['end']),
        } for value in values]

    return reservations


def list_reservations(start, end, *rooms):
    """
    Get the list of reservations for specified room names.

    :param start: start datetime to search
    :param end: end datetime to search
    :param rooms: list of rooms
    :return: reservations as a dictionary of roomname -> reservations
    """
    no_reservations = {}

    if not ready() or not rooms:
        return no_reservations

    startstr = format_date_param(start)
    endstr = format_date_param(end)
    roomnames = [room.external_name for room in rooms]

    returncode, out, err = run_cmd(
        'java', '-cp', settings.EXCHANGE_CONNECTOR_JAR, settings.EXCHANGE_LIST_CMD, startstr, endstr, *roomnames)

    if returncode != 0:
        return no_reservations

    return parse_reservations(out)


def create_reservation(start, end, room):
    if not ready():
        return

    startstr = format_date_param(start)
    endstr = format_date_param(end)
    roomname = room.external_name

    returncode, out, err = run_cmd(
        'java', '-cp', settings.EXCHANGE_CONNECTOR_JAR, settings.EXCHANGE_CREATE_CMD, startstr, endstr, roomname)


def cancel_reservation(start, end, room):
    if not ready():
        return

    epsilon = timedelta(minutes=1)
    startstr = format_date_param(start + epsilon)
    endstr = format_date_param(end - epsilon)
    roomname = room.external_name

    returncode, out, err = run_cmd(
        'java', '-cp', settings.EXCHANGE_CONNECTOR_JAR, settings.EXCHANGE_CANCEL_CMD, startstr, endstr, roomname)


def run_cmd(*args):
    pipes = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = pipes.communicate()

    return pipes.returncode, out.decode().strip(), err.decode().strip()

