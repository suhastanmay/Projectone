# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-22 07:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_remove_sensorreadings_detect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensorreadings',
            name='height',
        ),
    ]