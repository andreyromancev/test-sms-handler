# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-27 21:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=256)),
                ('request_data', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('phone', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestLogError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(null=True)),
                ('message', models.TextField(null=True)),
                ('log', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='error', to='handlers.RequestLog')),
            ],
        ),
    ]
