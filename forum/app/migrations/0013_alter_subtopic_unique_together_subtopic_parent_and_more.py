# Generated by Django 4.1.4 on 2023-01-23 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_subtopic_created_at_topic_created_at"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="subtopic",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="subtopic",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="app.subtopic",
            ),
        ),
        migrations.AlterField(
            model_name="subtopic",
            name="slug",
            field=models.SlugField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="subtopic",
            unique_together={("slug", "parent")},
        ),
        migrations.RemoveField(
            model_name="subtopic",
            name="topic",
        ),
        migrations.DeleteModel(
            name="Topic",
        ),
    ]