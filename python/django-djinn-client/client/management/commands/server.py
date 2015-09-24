from django.core.management.base import BaseCommand
from client.models import Config


class Command(BaseCommand):
    help = 'Interact with the server'

    def add_arguments(self, parser):
        parser.add_argument('--set-url', metavar='SERVER_URL', help='Set server URL')

    def print_server_url(self):
        self.stdout.write(Config.get_server_url())

    def set_server_url(self, server_url):
        # TODO validate first
        Config.set_server_url(server_url)

    def handle(self, *args, **options):
        if options['set_url']:
            self.set_server_url(options['set_url'])
        self.print_server_url()
