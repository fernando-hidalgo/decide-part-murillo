# Generated by Django 4.1 on 2023-11-27 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_auto_20180921_1119"),
        ("voting", "0006_questionbypreference_votingbypreference_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionYesNo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("desc", models.TextField()),
                ("optionYes", models.PositiveIntegerField(default=1, editable=False)),
                ("optionNo", models.PositiveIntegerField(default=2, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name="VotingYesNo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("desc", models.TextField(blank=True, null=True)),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("tally", models.JSONField(blank=True, null=True)),
                ("postproc", models.JSONField(blank=True, null=True)),
                (
                    "auths",
                    models.ManyToManyField(related_name="votingsyesno", to="base.auth"),
                ),
                (
                    "pub_key",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="votingyesno",
                        to="base.key",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votingyesno",
                        to="voting.questionyesno",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionOptionYesNo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.PositiveIntegerField(blank=True, null=True)),
                ("option", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pregYN",
                        to="voting.questionyesno",
                    ),
                ),
            ],
        ),
    ]
