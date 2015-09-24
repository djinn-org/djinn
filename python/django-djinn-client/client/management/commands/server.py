from django.core.management.base import BaseCommand
from client.models import Config


class Command(BaseCommand):
    help = 'Get and set server URL'

    def add_arguments(self, parser):
        parser.add_argument('--url', metavar='SERVER_URL', help='Set server URL')

    def print_server_url(self):
        self.stdout.write(Config.get_server_url())

    def set_server_url(self, server_url):
        # TODO validate first
        Config.set_server_url(server_url)

    def handle(self, *args, **options):
        if options['url']:
            self.set_server_url(options['url'])
        self.print_server_url()
