# Generated by Django 4.1.3 on 2022-11-30 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0009_customerdummy"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerdummy",
            name="image",
            field=models.ImageField(default=1, upload_to="customer_images"),
            preserve_default=False,
        ),
    ]