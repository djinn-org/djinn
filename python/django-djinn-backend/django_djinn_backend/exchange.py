from subprocess import Popen, PIPE

from django_djinn_backend import settings


def ready():
    return settings.EXCHANGE_CONNECTOR_READY


def list_reservations(rooms):
    if not ready():
        return rooms


def create_reservation(room, start, end):
    if not ready():
        return


def cancel_reservation(room, start, end):
    if not ready():
        return


def run_cmd(*args):
    pipes = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = pipes.communicate()

    return pipes.returncode, out.decode().strip(), err.decode().strip()

