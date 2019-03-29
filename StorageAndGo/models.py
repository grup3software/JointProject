from django.db import models

# Create your models here.

PRIORITY_TYPE = (
('A', 'Alta'),
('S', 'Sense Prioritat'),
)


class TaskMaintenance(models.Model):
    # HI HA TRES PRIORITATS
    priority = models.CharField('Priority', max_length=1, choices=PRIORITY_TYPE, default='A')
    room = models.ForeignKey("Room", default=1, on_delete=models.PROTECT)
    temperature = models.IntegerField(default=0)
    description = models.TextField(default="")
    user = models.ForeignKey("User", default="", on_delete=models.PROTECT, related_name="user")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room


class TaskOperator(models.Model):
    product = models.TextField(default="")
    origin = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="origin")
    destination = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="destination")
    quantity = models.ManyToManyField("Contenidor", default="")
    description = models.TextField()
    priority = models.CharField('Priority', max_length=1, choices=PRIORITY_TYPE, default='A')
    user = models.ForeignKey("User", default="", on_delete=models.PROTECT, related_name="user")

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
