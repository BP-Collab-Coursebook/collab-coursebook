# Generated by Django 3.0.4 on 2020-04-08 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_topic_content_tag_structure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Title'),
        ),
    ]
