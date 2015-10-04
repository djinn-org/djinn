from subprocess import Popen, PIPE

from django.core.management.base import BaseCommand
from client.models import Config
import urllib3
import certifi
import re


def create_http():
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where(),
    )
    return http


def put(url, params=None):
    return post_or_put(url, params, 'PUT')


def post(url, params=None):
    return post_or_put(url, params, 'POST')


def head(url):
    return create_http().request('HEAD', url).data.decode()


def post_or_put(url, params=None, method='POST'):
    if not params:
        params = {}

    http = create_http()
    resp = http.request(
        method,
        url,
        fields=params
    )
    return resp.data.decode()


class Command(BaseCommand):
    help = 'Interact with the server'

    def add_arguments(self, parser):
        parser.add_argument('--reset', metavar='IFACE', help='Reset MAC, IP, service URL')
        parser.add_argument('--set-server-url', metavar='SERVER_URL', help='Set server URL')
        parser.add_argument('--set-ip', metavar='IP', help='Set IP address')
        parser.add_argument('--set-mac', metavar='MAC', help='Set MAC address')
        parser.add_argument('--set-service-url', metavar='SERVICE_URL', help='Set service URL')
        parser.add_argument('--register', action='store_true')
        parser.add_argument('--send-presence', action='store_true')
        parser.add_argument('--send-empty', action='store_true')
        parser.add_argument('--send-heartbeat', action='store_true')

    def print_info(self):
        self.stdout.write('Server URL: {}'.format(Config.get_server_url()))
        self.stdout.write('IP: {}'.format(Config.get_ip()))
        self.stdout.write('MAC: {}'.format(Config.get_mac()))
        self.stdout.write('Service URL: {}'.format(Config.get_service_url()))

    def reset(self, iface):
        info = Popen(["/sbin/ifconfig", iface], stdout=PIPE).communicate()[0].decode()
        mac_match = re.findall(r'(ether|hwaddr) ([^ ]*)', info, re.I)
        if mac_match:
            mac = mac_match[0][1]
        else:
            self.stderr.write('Could not detect MAC address (incorrect interface?)')
            return

        ip_match = re.findall(r'inet (addr:)?([^ ]*)', info)
        if ip_match:
            ip = ip_match[0][1]
        else:
            self.stderr.write('Could not detect IP address (network down?)')
            return

        service_url = 'http://{}:{}/api/v1'.format(ip, 8001)
        Config.set_mac(mac)
        Config.set_ip(ip)
        Config.set_service_url(service_url)

    def register(self):
        mac = Config.get_mac()
        url = '{}/clients/{}/register'.format(Config.get_server_url(), mac)
        params = {
            'ip': Config.get_ip(),
            'mac': mac,
            'service_url': Config.get_service_url(),
        }
        response = post(url, params)
        self.stdout.write(response)

    def send_presence(self):
        url = '{}/clients/{}/presence'.format(Config.get_server_url(), Config.get_mac())
        response = put(url)
        self.stdout.write(response)

    def send_empty(self):
        url = '{}/clients/{}/empty'.format(Config.get_server_url(), Config.get_mac())
        response = put(url)
        self.stdout.write(response)

    def send_heartbeat(self):
        url = '{}/clients/{}/heartbeat'.format(Config.get_server_url(), Config.get_mac())
        response = head(url)
        self.stdout.write(response)

    def handle(self, *args, **options):
        should_print_info = False

        if options['reset']:
            self.reset(options['reset'])
            should_print_info = True

        if options['set_server_url']:
            Config.set_server_url(options['set_server_url'])
            should_print_info = True

        if options['set_ip']:
            Config.set_ip(options['set_ip'])
            should_print_info = True

        if options['set_mac']:
            Config.set_mac(options['set_mac'])
            should_print_info = True

        if options['set_service_url']:
            Config.set_service_url(options['set_service_url'])
            should_print_info = True

        if should_print_info:
            self.print_info()
        else:
            if options['register']:
                self.register()
            elif options['send_presence']:
                self.send_presence()
            elif options['send_empty']:
                self.send_empty()
            elif options['send_heartbeat']:
                self.send_heartbeat()
            else:
                self.print_info()
