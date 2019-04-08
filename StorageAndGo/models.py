from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PRIORITY_TYPE = (('A', 'Alta'),
                 ('S', 'Sense Prioritat'),)


class Task(models.Model):
    description = models.TextField(default="")
    user = models.ForeignKey(User, default="", on_delete=models.PROTECT, related_name="user_maintenance")


class TaskMaintenance(Task):
    # HI HA DOS PRIORITATS (AMB I SENSE)
    priority = models.CharField('Priority', max_length=1, choices=PRIORITY_TYPE, default='A')
    room = models.ForeignKey("Room", default=1, on_delete=models.PROTECT)
    temperature = models.IntegerField(default=0)


    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room


class TaskOperator(Task):
    product = models.TextField(default="")
    origin = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="origin")
    destination = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="destination")
    quantity = models.ManyToManyField("Contenidor", default="")
    priority = models.CharField('Priority', max_length=1, choices=PRIORITY_TYPE, default='A')

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
