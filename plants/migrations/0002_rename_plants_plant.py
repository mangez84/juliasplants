# Generated by Django 3.2.8 on 2021-10-30 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Plants',
            new_name='Plant',
        ),
    ]