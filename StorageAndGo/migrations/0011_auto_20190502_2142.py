# Generated by Django 2.1.7 on 2019-05-02 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StorageAndGo', '0010_task_hight_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='contenidorsInside',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='humitMax',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='humitMin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='temperatureMax',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='temperatureMin',
            field=models.IntegerField(default=0),
        ),
    ]
