# Generated by Django 2.1.2 on 2018-11-21 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_auto_20181121_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onpollclub',
            name='release_date',
            field=models.TimeField(default=datetime.datetime(2018, 11, 21, 9, 11, 40, 68286)),
        ),
    ]
