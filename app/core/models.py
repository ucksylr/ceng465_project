from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "events": [event.serialize() for event in Event.objects.filter(attendee_list__in=[self])]
        }


class Event(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=256)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendee_list = models.ManyToManyField(User)

    permissions = (
        ('delete_event', 'Delete Event'),
        ('add_event', 'Add Event'),
        ('change_event', 'Change Event'),
        ('can_enroll_event', 'Can Enroll Event'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
