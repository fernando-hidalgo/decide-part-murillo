# Generated by Django 4.1 on 2023-12-17 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_votemultichoice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vote',
            options={'verbose_name': 'Vote', 'verbose_name_plural': 'Votes'},
        ),
        migrations.AlterModelOptions(
            name='votebypreference',
            options={'verbose_name': 'Vote by Prefrence', 'verbose_name_plural': 'Votes by Preference'},
        ),
        migrations.AlterModelOptions(
            name='votemultichoice',
            options={'verbose_name': 'Vote Multi-Choice', 'verbose_name_plural': 'Votes Multi-Choice'},
        ),
        migrations.AlterModelOptions(
            name='voteyn',
            options={'verbose_name': 'Vote Yes No', 'verbose_name_plural': 'Votes Yes No'},
        ),
    ]