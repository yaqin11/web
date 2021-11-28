# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-21 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryId', models.CharField(max_length=20)),
                ('categoryName', models.CharField(max_length=40)),
                ('sort', models.CharField(max_length=20)),
                ('img', models.CharField(max_length=200)),
                ('product1', models.CharField(max_length=20)),
                ('product2', models.CharField(max_length=20)),
                ('product3', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'mainDescriptions',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('productId', models.CharField(max_length=30)),
                ('longName', models.CharField(max_length=150)),
                ('storeNums', models.CharField(max_length=30)),
                ('specifics', models.CharField(max_length=50)),
                ('sort', models.CharField(max_length=30)),
                ('marketPrice', models.CharField(max_length=30)),
                ('price', models.CharField(max_length=30)),
                ('categoryId', models.CharField(max_length=30)),
                ('childId', models.CharField(max_length=30)),
                ('img', models.CharField(max_length=200)),
                ('keywords', models.CharField(max_length=100)),
                ('brandId', models.CharField(max_length=30)),
                ('brandName', models.CharField(max_length=100)),
                ('safeDay', models.CharField(max_length=30)),
                ('safeUnit', models.CharField(max_length=30)),
                ('safeUnitDesc', models.CharField(max_length=30)),
                ('isDelete', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'products',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Slideshow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trackid', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('img', models.CharField(max_length=150)),
                ('sort', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'slideshows',
                'ordering': ['sort'],
            },
        ),
    ]