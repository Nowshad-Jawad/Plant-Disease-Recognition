# Generated by Django 3.1.6 on 2021-09-17 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0005_auto_20210918_0257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='username',
        ),
    ]