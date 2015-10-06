from django.db import models


class Config(models.Model):
    SERVER_URL = 'SERVER_URL'
    IP_ADDRESS = 'IP_ADDRESS'
    MAC_ADDRESS = 'MAC_ADDRESS'
    SERVICE_URL = 'SERVICE_URL'

    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return '{} = {}'.format(self.name, self.value)

    @staticmethod
    def get(name):
        try:
            return Config.objects.get(name=name).value
        except Config.DoesNotExist:
            return None

    @staticmethod
    def set(name, value):
        try:
            config = Config.objects.get(name=name)
            config.value = value
            config.save()
        except Config.DoesNotExist:
            Config.objects.create(name=name, value=value)

    @staticmethod
    def get_server_url():
        return Config.get(Config.SERVER_URL)

    @staticmethod
    def set_server_url(server_url):
        Config.set(Config.SERVER_URL, server_url)

    @staticmethod
    def get_ip():
        return Config.get(Config.IP_ADDRESS)

    @staticmethod
    def set_ip(ip):
        Config.set(Config.IP_ADDRESS, ip)

    @staticmethod
    def get_mac():
        return Config.get(Config.MAC_ADDRESS)

    @staticmethod
    def set_mac(mac):
        Config.set(Config.MAC_ADDRESS, mac)

    @staticmethod
    def get_service_url():
        return Config.get(Config.SERVICE_URL)

    @staticmethod
    def set_service_url(service_url):
        Config.set(Config.SERVICE_URL, service_url)


def make_choices(*values):
    return [(value, value.title()) for value in values]


class State(models.Model):
    STATE_NONE = 'none'
    STATE_PRESENCE = 'presence'
    STATE_EMPTY = 'empty'

    state = models.CharField(max_length=50, default=STATE_NONE,
                             choices=make_choices(STATE_NONE, STATE_EMPTY, STATE_PRESENCE))

    def __str__(self):
        return self.state

    @staticmethod
    def is_state(state):
        try:
            State.objects.first() == state
        except State.DoesNotExist:
            return False

    @staticmethod
    def is_presence():
        return State.is_state(State.STATE_PRESENCE)

    @staticmethod
    def is_empty():
        return State.is_state(State.STATE_PRESENCE)

    @staticmethod
    def set_state(state):
        State.objects.all().delete()
        State.objects.create(state=state)

    @staticmethod
    def set_presence():
        State.set_state(State.STATE_PRESENCE)

    @staticmethod
    def set_empty():
        State.set_state(State.STATE_EMPTY)

    @staticmethod
    def set_none():
        State.set_state(State.STATE_NONE)

    @staticmethod
    def get_state():
        return State.objects.first() or State.STATE_NONE
