# Generated by Django 4.2.4 on 2023-08-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandTool', '0022_repo_architectures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repo',
            name='architectures',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='repo',
            name='components',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='repo',
            name='dist',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='repo',
            name='mirrorName',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]
