# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-22 03:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_categoriegroup_childgroup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoriegroup',
            options={'ordering': ['sort']},
        ),
        migrations.AlterModelTable(
            name='categoriegroup',
            table='categoriegroups',
        ),
    ]