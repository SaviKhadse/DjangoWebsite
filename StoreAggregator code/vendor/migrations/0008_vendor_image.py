# Generated by Django 4.1.2 on 2022-12-07 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0007_alter_vendor_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="image",
            field=models.ImageField(default=1, upload_to="vendor_images"),
            preserve_default=False,
        ),
    ]
