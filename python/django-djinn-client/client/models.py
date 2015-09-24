from django.db import models


class Config(models.Model):
    SERVER_URL = 'SERVER_URL'

    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return '{} = {}'.format(self.name, self.value)

    @staticmethod
    def get_server_url():
        try:
            return Config.objects.get(name=Config.SERVER_URL).value
        except Config.DoesNotExist:
            return None

    @staticmethod
    def set_server_url(server_url):
        try:
            config = Config.objects.get(name=Config.SERVER_URL)
            config.value = server_url
            config.save()
        except Config.DoesNotExist:
            Config.objects.create(name=Config.SERVER_URL, value=server_url)
