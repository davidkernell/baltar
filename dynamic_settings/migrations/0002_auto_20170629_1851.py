# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 18:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamictradesetting',
            name='coin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dynamic_settings.Coin'),
        ),
    ]