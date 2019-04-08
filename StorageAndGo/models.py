from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PRIORITY_TYPE = (('A', 'Alta'),
                 ('S', 'Sense Prioritat'),)


class Task(models.Model):
    description = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_maintenance", blank=True, null=True)


class TaskMaintenance(Task):
    # HI HA DOS PRIORITATS (AMB I SENSE)
    priority = models.CharField('Priority', max_length=1, choices=PRIORITY_TYPE, blank=True, null=True)
    room = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, blank=True, null=True)
    temperature = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room

    def get_class(self):
        return TaskMaintenance.__class__

class TaskOperator(Task):
    product = models.TextField(default="", blank=True)
    origin = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="origin", blank=True, null=True)
    destination = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="destination", blank=True, null=True)
    quantity = models.ManyToManyField("Contenidor", default="", blank=True, null=True)
    priority = models.CharField('Priority', max_length=1, choices=PRIORITY_TYPE, blank=True)

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.description


class Contenidor(models.Model):
    description = models.TextField(default="")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.description


class Room(models.Model):
    description = models.TextField(default="")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.description
