# Generated by Django 4.2.3 on 2023-07-11 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commandTool', '0017_remove_result_execution_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='message',
        ),
    ]