# Generated by Django 2.1.7 on 2019-04-26 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StorageAndGo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenidor',
            name='sla',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='manifesto',
            name='revisionDate',
            field=models.DateTimeField(null=True),
        ),
    ]
