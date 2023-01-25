# Generated by Django 4.1.4 on 2023-01-23 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014_rename_parent_subtopic_topic_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subtopic",
            name="slug",
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name="subtopic",
            name="topic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app.subtopic",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="thread",
            unique_together={("slug", "subtopic")},
        ),
    ]
