# Generated by Django 2.1.7 on 2019-04-10 07:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('name', models.CharField(max_length=200, null=True)),
                ('temp_min', models.SmallIntegerField(null=True)),
                ('temp_max', models.SmallIntegerField(null=True)),
                ('moistness_min', models.PositiveSmallIntegerField(null=True)),
                ('moistness_max', models.PositiveSmallIntegerField(null=True)),
                ('limit_date', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manifesto',
            fields=[
                ('reference', models.BigIntegerField(default=0, primary_key=True, serialize=False)),
                ('entry_date', models.DateField(default=datetime.date.today)),
                ('origin', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('accepted', models.BooleanField(default=False)),
                ('priority', models.CharField(blank=True, choices=[('A', 'Alta'), ('S', 'Sense Prioritat')], max_length=1, null=True, verbose_name='Priority')),
            ],
        ),
        migrations.CreateModel(
            name='TaskMaintenance',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='StorageAndGo.Task')),
                ('temperature', models.IntegerField(blank=True, default=0)),
                ('room', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='StorageAndGo.Room')),
            ],
            bases=('StorageAndGo.task',),
        ),
        migrations.CreateModel(
            name='TaskOperator',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='StorageAndGo.Task')),
                ('product', models.TextField(blank=True, default='')),
                ('destination', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='destination', to='StorageAndGo.Room')),
                ('origin', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origin', to='StorageAndGo.Room')),
            ],
            bases=('StorageAndGo.task',),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_maintenance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contenidor',
            name='manifesto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StorageAndGo.Manifesto'),
        ),
        migrations.AddField(
            model_name='taskoperator',
            name='quantity',
            field=models.ManyToManyField(blank=True, default='', to='StorageAndGo.Contenidor'),
        ),
    ]
