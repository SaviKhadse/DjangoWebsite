# Generated by Django 4.1.2 on 2022-10-25 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_alter_product_estimated_tax"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]