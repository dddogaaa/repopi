# Generated by Django 4.2.3 on 2023-07-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandTool', '0015_alter_result_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='file',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]
