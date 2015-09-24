from django.db import models


class Config(models.Model):
    SERVER_URL = 'SERVER_URL'

    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return '{} = {}'.format(self.name, self.value)

    def get_server_url(self):
        return Config.objects.get(name=self.SERVER_URL)

    def set_server_url(self, server_url):
        config = Config.objects.get(name=self.SERVER_URL)
        config.value = server_url
        config.save()
