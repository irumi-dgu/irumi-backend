# Generated by Django 4.2.5 on 2023-09-20 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lantern", "0007_lantern_light_bool_alter_report_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="key",
            field=models.CharField(default="9rsKguNUZX", max_length=10),
        ),
    ]