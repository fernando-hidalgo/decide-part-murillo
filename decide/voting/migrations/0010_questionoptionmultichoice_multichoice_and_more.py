# Generated by Django 4.1 on 2023-12-14 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0009_questionmultichoice_votingmultichoice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionoptionmultichoice',
            name='multichoice',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionoptionmultichoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multichoices', to='voting.questionmultichoice'),
        ),
        migrations.AlterField(
            model_name='votingmultichoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votingmultichoice', to='voting.questionmultichoice'),
        ),
    ]
