# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 00:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyInstagram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscriptions',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
