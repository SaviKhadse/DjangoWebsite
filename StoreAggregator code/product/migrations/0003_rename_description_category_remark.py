# Generated by Django 4.1.2 on 2022-10-25 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_category_product_store_category_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category", old_name="description", new_name="remark",
        ),
    ]