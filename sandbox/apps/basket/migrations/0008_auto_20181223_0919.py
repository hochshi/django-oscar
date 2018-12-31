# Generated by Django 2.1.4 on 2018-12-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0007_slugfield_noop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineattribute',
            name='value',
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_boolean',
            field=models.NullBooleanField(verbose_name='Boolean'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='DateTime'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='images/products/%Y/%m/'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_float',
            field=models.FloatField(blank=True, null=True, verbose_name='Float'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='images/products/%Y/%m/'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_integer',
            field=models.IntegerField(blank=True, null=True, verbose_name='Integer'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_richtext',
            field=models.TextField(blank=True, null=True, verbose_name='Richtext'),
        ),
        migrations.AddField(
            model_name='lineattribute',
            name='value_text',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
    ]