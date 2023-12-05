# Generated by Django 4.1.7 on 2023-02-22 00:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                ("name", models.TextField()),
                ("description", models.TextField()),
                ("status", models.IntegerField(default=1)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Products",
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
                ("code", models.CharField(max_length=100)),
                ("name", models.TextField()),
                ("description", models.TextField()),
                ("price", models.IntegerField(default=0)),
                ("status", models.IntegerField(default=1)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("units", models.IntegerField(default=1)),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="posApp.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sales",
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
                ("is_credit", models.BooleanField(default=False)),
                ("client_name", models.CharField(default=None, max_length=200)),
                ("cooperative_number", models.CharField(default=None, max_length=100)),
                ("code", models.CharField(max_length=100)),
                ("sub_total", models.FloatField(default=0)),
                ("grand_total", models.FloatField(default=0)),
                ("tax_amount", models.FloatField(default=0)),
                ("tax", models.FloatField(default=0)),
                ("tendered_amount", models.FloatField(default=0)),
                ("amount_change", models.FloatField(default=0)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_created", models.DateField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="salesItems",
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
                ("price", models.FloatField(default=0)),
                ("qty", models.FloatField(default=0)),
                ("total", models.FloatField(default=0)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="posApp.products",
                    ),
                ),
                (
                    "sale_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posApp.sales"
                    ),
                ),
            ],
        ),
    ]
