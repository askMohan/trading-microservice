# Generated by Django 4.2.11 on 2024-04-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("quantity", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=20)),
                ("side", models.IntegerField(choices=[(1, "BUY"), (-1, "SELL")])),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "OPEN"),
                            (2, "PARTIALLY_FILLED"),
                            (3, "SUCCESSFULL"),
                            (4, "UNSUCCESSFULL"),
                            (5, "CANCELLED"),
                        ],
                        default=1,
                    ),
                ),
                ("traded_quantity", models.IntegerField(default=0)),
                (
                    "average_traded_price",
                    models.DecimalField(decimal_places=2, max_digits=20, null=True),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
