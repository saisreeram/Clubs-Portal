# Generated by Django 2.1.2 on 2018-12-09 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20181208_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='event_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='events',
            name='event_to',
            field=models.DateField(),
        ),
    ]
