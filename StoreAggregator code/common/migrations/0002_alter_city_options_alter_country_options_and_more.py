# Generated by Django 4.1.2 on 2022-11-18 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="city", options={"ordering": ["id"], "verbose_name_plural": "City"},
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"ordering": ["id"], "verbose_name_plural": "Country"},
        ),
        migrations.AlterModelOptions(
            name="state", options={"ordering": ["id"], "verbose_name_plural": "State"},
        ),
    ]
