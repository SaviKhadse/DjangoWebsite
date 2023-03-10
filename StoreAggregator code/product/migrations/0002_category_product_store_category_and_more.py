# Generated by Django 4.1.2 on 2022-10-25 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("description", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="store_category",
            field=models.CharField(
                choices=[("med", "Medicine"), ("gro", "Grocery")],
                default="gro",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="product.category"
            ),
        ),
    ]
