# Generated by Django 2.2.1 on 2019-06-17 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_statictoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StaticToken',
        ),
    ]
