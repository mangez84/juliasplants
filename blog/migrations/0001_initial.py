# Generated by Django 3.2.8 on 2021-11-14 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plants', '0004_alter_plant_discount_price'),
        ('profiles', '0006_alter_userprofilecomment_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plants.plant')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile')),
            ],
            options={
                'verbose_name_plural': 'Blog Posts',
            },
        ),
    ]
