# Generated by Django 4.2.5 on 2023-09-22 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lantern', '0007_lantern_light_bool_alter_report_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='key',
            field=models.CharField(default='LRz6EScOf7', max_length=10),
        ),
    ]
