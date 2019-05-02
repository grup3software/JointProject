from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse

# Create your models here.


class Task(models.Model):
    description = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_maintenance", blank=True, null=True)
    accepted = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    hight_priority = models.BooleanField(default=False)

    def get_class(self):
        # return self.__class__.__name__
        return ""

    def get_absolute_url(self):
        # return reverse('storageandgo:task_list', kwargs={'pk': self.pk})
        return reverse('storageandgo:task_list')


# HI HA TRES TIPUS DE SUBCLASSE DE MANTENIMENT
class TaskMaintenance(Task):
    # HI HA DOS PRIORITATS (AMB I SENSE)
    room = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, blank=True, null=True)
    temperature = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.room

    def get_class(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        # return reverse('storageandgo:task_list', kwargs={'pk': self.pk})
        return reverse('storageandgo:task_list')


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

    def get_absolute_url(self):
        # return reverse('storageandgo:task_list', kwargs={'pk': self.pk})
        return reverse('storageandgo:task_list')


class Manifesto(models.Model):
    ref = models.CharField(primary_key=True, default="", max_length=50)
    creationDate = models.DateTimeField(default=date.today)
    revisionDate = models.DateTimeField(null=True)
    withdrawal = models.BooleanField(null=True)
    totalpackets = models.IntegerField(null=True)
    fromLocation = models.CharField(max_length=255)
    toLocation = models.CharField(max_length=255)
    Products = models.ManyToManyField('Contenidor', related_name='Products')

    def create_manifesto(self, diccionari):
        self.objects.create(reference=diccionari['ref'],
                            entry_date=diccionari['creationDate'],
                            revision_date=diccionari['revisionDate'],
                            withdraw=diccionari['withdrawal'],
                            number_packets=diccionari['totalpackets'],
                            origin=diccionari['fromLocation'],
                            destination=diccionari['toLocation'])

    def get_length(self):
        return Contenidor.objects.filter(Contenidor.manifesto == self.ref).count()

    def get_different_products(self):
        return Contenidor.objects.filter(Contenidor.manifesto == self.ref).distinct(Contenidor.name).count()

    def __unicode__(self):
        return u"%s" % self.name


class Contenidor(models.Model):
    name = models.CharField(max_length=200, null=True)
    qty = models.IntegerField(null=True)
    tempMinDegree = models.SmallIntegerField(null=True, validators=[MinValueValidator(-30),
                                                                    MaxValueValidator(30)])
    tempMaxDegree = models.SmallIntegerField(null=True, validators=[MinValueValidator(-30),
                                                                    MaxValueValidator(30)])
    humidMin = models.PositiveSmallIntegerField(null=True, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(100)])
    humidMax = models.PositiveSmallIntegerField(null=True, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(100)])
    sla = models.DateTimeField(null=True)
    # manifesto = models.ForeignKey(Manifesto, on_delete=models.CASCADE, null=True)

    def create_container(self, diccionari):
        self.objects.create(name=diccionari['name'],
                            quantity=diccionari['quantity'],
                            temp_min=diccionari['temp_min'],
                            temp_max=diccionari['temp_max'],
                            moistness_min=diccionari['moistness_min'],
                            limit_date=diccionari['limit_date'],
                            manifesto=diccionari['manifesto'])

    def delete_container(self):
        Contenidor.objects.filter(self.id).delete()

    def __unicode__(self):
        return u"%s" % self.name


class Room(models.Model):
    name = models.CharField(max_length=200,null=True)
    description = models.TextField(default="")

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.description


class Avaria(Task):
    room = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, blank=True, null=True)
    object = models.TextField(default="", blank=True)

    def __unicode__(self):
        return self.description
