# Generated by Django 4.1 on 2023-12-04 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0009_voting_question_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting',
            name='question_option',
        ),
    ]