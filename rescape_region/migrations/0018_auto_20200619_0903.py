# Generated by Django 3.0.5 on 2020-06-19 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rescape_region', '0017_auto_20200618_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='updated_at',
        ),
    ]
