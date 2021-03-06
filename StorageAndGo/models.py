from django.utils.timezone import now

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class Task(models.Model):
    description = models.TextField(default="", verbose_name='Descripción')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_maintenance", blank=True, null=True,
                             verbose_name='Usuario')
    accepted = models.BooleanField(default=False, verbose_name='Acceptado')
    finished = models.BooleanField(default=False, verbose_name='Acabado')
    high_priority = models.BooleanField(default=False, verbose_name='Alta prioridad')

    def __str__(self):
        return str(self.pk) + " - " + self.description

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
    temperature = models.IntegerField(default=0, blank=True, verbose_name='Temperatura')

    def __str__(self):
        return str(self.pk) + " - " + self.description

    def get_class(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        # return reverse('storageandgo:task_list', kwargs={'pk': self.pk})
        return reverse('storageandgo:task_list')


class TaskOperator(Task):
    product = models.TextField(default="", blank=True, verbose_name='Producto')
    origin = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="origin", blank=True,
                               null=True, verbose_name='Origen')
    destination = models.ForeignKey("Room", default=1, on_delete=models.PROTECT, related_name="destination", blank=True,
                                    null=True, verbose_name='Destino')
    quantity = models.IntegerField(null=False, default=0, verbose_name='Cantidad')

    def __str__(self):
        return str(self.pk) + " - " + self.description

    def get_class(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        # return reverse('storageandgo:task_list', kwargs={'pk': self.pk})
        return reverse('storageandgo:task_list')


class Manifesto(models.Model):
    ref = models.CharField(primary_key=True, default="", max_length=50, verbose_name='Referencia')
    creationDate = models.DateTimeField(default=now, verbose_name='Fecha de creación')
    revisionDate = models.DateTimeField(null=True, verbose_name='Fecha de revisión')
    withdrawal = models.BooleanField(null=True, verbose_name='Salida')
    totalpackets = models.IntegerField(null=True, verbose_name='Numero total de paquetes')
    fromLocation = models.CharField(max_length=255, verbose_name='Des de')
    toLocation = models.CharField(max_length=255, verbose_name='Para')
    products = models.ManyToManyField('Contenidor', related_name='Products', verbose_name='Productos')

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

    def __str__(self):
        return self.ref


class Contenidor(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name='Nombre contenedor')
    qty = models.IntegerField(null=True, verbose_name='Cantidad')
    tempMinDegree = models.SmallIntegerField(null=True, validators=[MinValueValidator(-30),
                                                                    MaxValueValidator(30)],
                                             verbose_name='Temperatura mínima')
    tempMaxDegree = models.SmallIntegerField(null=True, validators=[MinValueValidator(-30),
                                                                    MaxValueValidator(30)],
                                             verbose_name='Temperatura máxima')
    humidMin = models.PositiveSmallIntegerField(null=True, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(100)],
                                                verbose_name='Humedad mínima')
    humidMax = models.PositiveSmallIntegerField(null=True, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(100)],
                                                verbose_name='Humedad máxima')
    sla = models.DateTimeField(null=True)

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

    def __str__(self):
        return str(self.pk) + " - " + self.name + " - " + str(self.qty)


class Room(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name='Nombre sala')
    temperatureMin = models.IntegerField("Temperatura mínima", null=False, default=0)
    temperatureMax = models.IntegerField("Temperatura máxima", null=False, default=0)
    humitMin = models.IntegerField("Humedad mínima", null=False, default=0)
    humitMax = models.IntegerField("Humedad máxima", null=False, default=0)
    capacity = models.PositiveSmallIntegerField("Capacidad", null=False, validators=[MinValueValidator(1)])
    contenidorsInside = models.IntegerField("Contenedores Dentro", null=False, default=0)
    description = models.TextField("Descripción", default="", null=True)

    def __unicode__(self):
        # return u"%d - %d - %s" % self.room, self.temperature, self.description
        return u"%s" % self.description

    def get_absolute_url(self):
        return reverse('storageandgo:sala_detail', kwargs={'pk': self.pk})

    def percent_ocupation(self):
        return (100 * self.contenidorsInside) / self.capacity

    def __str__(self):
        return self.name


class Avaria(Task):
    room = models.ForeignKey('Room', default=1, on_delete=models.PROTECT, blank=True, null=True)
    object = models.TextField('Pieza', default="", blank=True)

    def __str__(self):
        return str(self.pk) + " - " + self.room.name
