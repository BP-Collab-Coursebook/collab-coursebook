# Generated by Django 3.0.7 on 2021-02-19 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20210206_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='latex',
            options={'verbose_name': 'Latex Content', 'verbose_name_plural': 'Latex Contents'},
        ),
        migrations.AlterField(
            model_name='latex',
            name='textfield',
            field=models.TextField(verbose_name='Latex Code'),
        ),
    ]
