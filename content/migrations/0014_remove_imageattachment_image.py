# Generated by Django 3.0.7 on 2021-01-07 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0013_auto_20210106_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageattachment',
            name='image',
        ),
    ]
