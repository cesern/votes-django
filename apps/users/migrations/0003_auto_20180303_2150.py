# Generated by Django 2.0.2 on 2018-03-04 04:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20180303_1918'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Emplooyee',
        ),
    ]
