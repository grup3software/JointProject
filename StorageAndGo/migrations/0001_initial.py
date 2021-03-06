# Generated by Django 2.1.7 on 2019-06-10 13:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contenidor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Nombre contenedor')),
                ('qty', models.IntegerField(null=True, verbose_name='Cantidad')),
                ('tempMinDegree', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)], verbose_name='Temperatura mínima')),
                ('tempMaxDegree', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(-30), django.core.validators.MaxValueValidator(30)], verbose_name='Temperatura máxima')),
                ('humidMin', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Humedad mínima')),
                ('humidMax', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Humedad máxima')),
                ('sla', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manifesto',
            fields=[
                ('ref', models.CharField(default='', max_length=50, primary_key=True, serialize=False, verbose_name='Referencia')),
                ('creationDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creación')),
                ('revisionDate', models.DateTimeField(null=True, verbose_name='Fecha de revisión')),
                ('withdrawal', models.BooleanField(null=True, verbose_name='Salida')),
                ('totalpackets', models.IntegerField(null=True, verbose_name='Numero total de paquetes')),
                ('fromLocation', models.CharField(max_length=255, verbose_name='Des de')),
                ('toLocation', models.CharField(max_length=255, verbose_name='Para')),
                ('products', models.ManyToManyField(related_name='Products', to='StorageAndGo.Contenidor', verbose_name='Productos')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Nombre sala')),
                ('temperatureMin', models.IntegerField(default=0, verbose_name='Temperatura mínima')),
                ('temperatureMax', models.IntegerField(default=0, verbose_name='Temperatura máxima')),
                ('humitMin', models.IntegerField(default=0, verbose_name='Humedad mínima')),
                ('humitMax', models.IntegerField(default=0, verbose_name='Humedad máxima')),
                ('capacity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Capacidad')),
                ('contenidorsInside', models.IntegerField(default=0, verbose_name='Contenedores Dentro')),
                ('description', models.TextField(default='', null=True, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='', verbose_name='Descripción')),
                ('accepted', models.BooleanField(default=False, verbose_name='Acceptado')),
                ('finished', models.BooleanField(default=False, verbose_name='Acabado')),
                ('hight_priority', models.BooleanField(default=False, verbose_name='Alta prioridad')),
            ],
        ),
        migrations.CreateModel(
            name='Avaria',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='StorageAndGo.Task')),
                ('object', models.TextField(blank=True, default='', verbose_name='Objecto')),
                ('room', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='StorageAndGo.Room')),
            ],
            bases=('StorageAndGo.task',),
        ),
        migrations.CreateModel(
            name='TaskMaintenance',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='StorageAndGo.Task')),
                ('temperature', models.IntegerField(blank=True, default=0, verbose_name='Temperatura')),
                ('room', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='StorageAndGo.Room')),
            ],
            bases=('StorageAndGo.task',),
        ),
        migrations.CreateModel(
            name='TaskOperator',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='StorageAndGo.Task')),
                ('product', models.TextField(blank=True, default='', verbose_name='Producto')),
                ('quantity', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('destination', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='destination', to='StorageAndGo.Room', verbose_name='Destino')),
                ('origin', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origin', to='StorageAndGo.Room', verbose_name='Origen')),
            ],
            bases=('StorageAndGo.task',),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_maintenance', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
