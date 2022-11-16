from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Room(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    name = models.CharField(max_length=100, default=None, null=True)
    updated = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='room_to_user')


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='message_to_room')
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_to_user')

class Profile(models.Model):
    name = models.CharField(max_length=100, default="Anonymous")
    image = models.ImageField(
        default='marina.jpg',
        upload_to='profile_pics'
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def __create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(__create_profile, sender=User)