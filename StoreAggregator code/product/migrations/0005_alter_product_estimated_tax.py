# Generated by Django 4.1.2 on 2022-10-25 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_alter_category_remark"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="estimated_tax",
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]