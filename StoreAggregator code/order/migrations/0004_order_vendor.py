# Generated by Django 4.1.2 on 2022-12-08 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0008_vendor_image"),
        ("order", "0003_order_delivery_charges"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="vendor",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="vendor.vendor",
            ),
            preserve_default=False,
        ),
    ]