# Generated by Django 3.1.6 on 2021-03-05 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_create_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='working_address',
        ),
    ]
