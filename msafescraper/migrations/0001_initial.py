# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_id', models.SmallIntegerField()),
                ('dev_blog', models.BooleanField(default=False)),
            ],
        ),
    ]
