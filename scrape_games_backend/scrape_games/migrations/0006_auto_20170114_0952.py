# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-14 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape_games', '0005_auto_20170114_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmodel',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]