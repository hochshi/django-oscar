# Generated by Django 2.1.4 on 2018-12-24 04:24

import apps.basket.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0008_auto_20181223_0919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineattribute',
            options={},
        ),
        migrations.AlterField(
            model_name='lineattribute',
            name='value_file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=apps.basket.models.upload_to),
        ),
        migrations.AlterField(
            model_name='lineattribute',
            name='value_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=apps.basket.models.upload_to),
        ),
    ]