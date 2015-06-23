from argparse import ArgumentParser
from datetime import datetime
from mrgenie.parsecom.services import ParseService
from mrgenie.utils import status


CMD_ROOMS = 'rooms'
CMD_RESERVATIONS = 'reservations'
CMD_STATUS = 'status'

SERVICES = {
    'parse': ParseService(),
    'koua': ParseService()
}

COMMANDS = [
    CMD_ROOMS,
    CMD_RESERVATIONS,
    CMD_STATUS
]


def print_rooms(service):
    for room in service.get_rooms():
        print('id: {} name: {}'.format(*room))


def print_reservations(service, room_id):
    for reservation in service.get_reservations(room_id):
        print(reservation)


def print_status(service, room_id):
    date = datetime.now()
    reservations = service.get_reservations(room_id)
    print(status.get_status(reservations, date))


def print_all_status(service):
    date = datetime.now()
    for room in service.get_rooms():
        room_id = room[0]
        reservations = service.get_reservations(room_id)
        print('id: {} status: {}'.format(room_id, status.get_status(reservations, date)))


def main():
    parser = ArgumentParser(description='Meeting Room Genie CLI')
    parser.add_argument('service', choices=SERVICES.keys())
    parser.add_argument('cmd', choices=COMMANDS)
    parser.add_argument('--room-id', '-r')

    args = parser.parse_args()

    service = SERVICES[args.service]

    if args.cmd == CMD_ROOMS:
        print_rooms(service)
    elif args.cmd == CMD_RESERVATIONS:
        print_reservations(service, args.room_id)
    elif args.cmd == CMD_STATUS:
        if args.room_id:
            print_status(service, args.room_id)
        else:
            print_all_status(service)

if __name__ == '__main__':
    main()
