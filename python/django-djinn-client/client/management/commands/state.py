from django.core.management.base import BaseCommand
from client.models import State


class Command(BaseCommand):
    help = 'Check and update state'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Reset state')
        parser.add_argument('--set-state', metavar='STATE', help='Reset state')

    def print_info(self):
        self.stdout.write('State: {}'.format(State.get_state()))

    def reset(self):
        State.set_none()

    def set(self, state):
        State.set_state(state)

    def handle(self, *args, **options):
        if options['set_state']:
            self.set(options['set_state'])
        if options['reset']:
            self.reset()

        self.print_info()
