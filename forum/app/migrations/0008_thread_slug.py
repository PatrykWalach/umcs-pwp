# Generated by Django 4.1.4 on 2023-01-22 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_post_content_subtopic_name_subtopic_slug_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="thread",
            name="slug",
            field=models.SlugField(default="Title", max_length=150),
            preserve_default=False,
        ),
    ]
