# Generated by Django 3.2.8 on 2022-12-08 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reader',
            name='last_name',
            field=models.CharField(default='Doe', max_length=100),
        ),
    ]
