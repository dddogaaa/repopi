# Generated by Django 4.2.3 on 2023-07-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandTool', '0014_result_delete_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
