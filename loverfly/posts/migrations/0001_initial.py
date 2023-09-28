# Generated by Django 4.1.7 on 2023-08-17 11:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("couples", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
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
                (
                    "time_posted",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("caption", models.CharField(blank=True, max_length=25, null=True)),
                ("image", models.CharField(blank=True, max_length=1000, null=True)),
                ("likes", models.PositiveBigIntegerField(blank=True, default=0)),
                ("deleted", models.BooleanField(default=False)),
                ("deleted_date", models.DateField(default=django.utils.timezone.now)),
                (
                    "couple",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_owner",
                        to="couples.couple",
                    ),
                ),
            ],
            options={
                "get_latest_by": "time_posted",
            },
        ),
    ]
