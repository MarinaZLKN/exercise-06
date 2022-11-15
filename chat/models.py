from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    name = models.CharField(max_length=100, default=None)
    updated = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='room_to_user')
