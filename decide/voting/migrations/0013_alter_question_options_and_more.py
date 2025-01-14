# Generated by Django 4.1 on 2023-12-17 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0012_merge_0011_merge_20231215_1206_0011_voting_mixnet_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questionbypreference',
            options={'verbose_name': 'Question by Prefrence', 'verbose_name_plural': 'Questions by Prefrence'},
        ),
        migrations.AlterModelOptions(
            name='questionmultichoice',
            options={'verbose_name': 'Question Multi-Choice', 'verbose_name_plural': 'Questions Multi-Choice'},
        ),
        migrations.AlterModelOptions(
            name='questionyesno',
            options={'verbose_name': 'Question Yes No', 'verbose_name_plural': 'Questions Yes No'},
        ),
        migrations.AlterModelOptions(
            name='voting',
            options={'verbose_name': 'Voting', 'verbose_name_plural': 'Votings'},
        ),
        migrations.AlterModelOptions(
            name='votingbypreference',
            options={'verbose_name': 'Voting by Prefrence', 'verbose_name_plural': 'Votings by Prefrence'},
        ),
        migrations.AlterModelOptions(
            name='votingmultichoice',
            options={'verbose_name': 'Voting Multi-Choice', 'verbose_name_plural': 'Votings Multi-Choice'},
        ),
        migrations.AlterModelOptions(
            name='votingyesno',
            options={'verbose_name': 'Voting Yes No', 'verbose_name_plural': 'Votings Yes No'},
        ),
        migrations.AddField(
            model_name='questionoptionmultichoice',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
