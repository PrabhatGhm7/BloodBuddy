from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.TextField()
class Message(models.Model):
    value = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.TextField()
    room = models.TextField()