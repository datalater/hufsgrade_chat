# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-22 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='kakao_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_key', models.CharField(max_length=50)),
                ('step', models.IntegerField(default=0)),
                ('hufs_id', models.CharField(max_length=25)),
                ('hufs_pwd', models.CharField(max_length=25)),
            ],
        ),
    ]
