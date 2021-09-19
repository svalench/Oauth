from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    client_id = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=100, unique=True)
    default_redirect_uri = models.TextField()
    is_active = models.BooleanField(default=False, blank=True)
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)


    def client_exist(self, client_id):
        if self._meta.model.objects.filter(client_id=client_id).exists():
            return True
        return False


class ClientsCodes(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)

