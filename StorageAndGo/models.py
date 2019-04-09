from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

PRIORITY_TYPE = (('A', 'Alta'),
                 ('S', 'Sense Prioritat'),)


class Task(models.Model):
    description = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_maintenance", blank=True, null=True)
    accepted = models.BooleanField(default=False)
    priority = models.CharField('Priority', max_length=1, choices=PRIORITY_TYPE, blank=True, null=True)

    def get_class(self):
        # return self.__class__.__name__
        return ""


class TaskMaintenance(Task):
    # HI HA DOS PRIORITATS (AMB I SENSE)
    room = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, blank=True, null=True)
    temperature = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room

    def get_class(self):
        return self.__class__.__name__


class TaskOperator(Task):
    product = models.TextField(default="", blank=True)
    origin = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="origin", blank=True, null=True)
    destination = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="destination", blank=True, null=True)
    quantity = models.ManyToManyField("Contenidor", default="", blank=True)

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.description

    def get_class(self):
        return self.__class__.__name__


class Manifesto(models.Model):
    reference = models.BigIntegerField(primary_key=True, default=00000000000)
    entry_date = models.DateField(default=date.today)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    def get_length(self):
        return Contenidor.objects.filter(Contenidor.manifesto == self.reference).count()

    def get_different_products(self):
        return Contenidor.objects.filter(Contenidor.manifesto == self.reference).distinct(Contenidor.name).count()

    def __unicode__(self):
        return u"%s" % self.name


class Contenidor(models.Model):
    name = models.CharField(max_length=200, null=True)
    temp_min = models.SmallIntegerField(null=True)
    temp_max = models.SmallIntegerField(null=True)
    moistness_min = models.PositiveSmallIntegerField(null=True)
    moistness_max = models.PositiveSmallIntegerField(null=True)
    limit_date = models.DateField(default=None, null=True)
    manifesto = models.ForeignKey(Manifesto, on_delete=models.CASCADE, null=True)

    def create_container(self, name, temp_min, temp_max, moistness_min, limit_date, manifesto):
        self.objects.create(name=name, temp_min=temp_min, temp_max=temp_max, moistness_min=moistness_min, limit_date=limit_date, manifesto=manifesto)

    def delete_container(self):
        Contenidor.objects.filter(self.id).delete()

    def __unicode__(self):
        return u"%s" % self.name


class Room(models.Model):
    description = models.TextField(default="")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.description
