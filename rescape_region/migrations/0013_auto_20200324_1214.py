# Generated by Django 2.0.7 on 2020-03-24 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescape_region', '0012_auto_20200227_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='key',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
