# Generated by Django 4.1.4 on 2023-01-23 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0011_alter_topic_slug_alter_subtopic_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="subtopic",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
