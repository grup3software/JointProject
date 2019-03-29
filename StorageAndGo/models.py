from django.db import models

# Create your models here.


class TaskMaintenance(models.Model):
    # HI HA TRES PRIORITATS
    priority = models.IntegerField(choices=)
    room = models.ForeignKey("Room", default=1, on_delete=models.PROTECT)
    temperature = models.IntegerField(default=0)
    description = models.TextField(default="")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room


class TaskOperator(models.Model):
    product = models.TextField(default="")
    origin = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="origin")
    destination = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="destination")
    quantity = models.ManyToManyField("Container", default="")
    description = models.TextField()

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room


class Container(models.Model):
    description = models.TextField(default="")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room


class Room(models.Model):
    description = models.TextField(default="")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room
