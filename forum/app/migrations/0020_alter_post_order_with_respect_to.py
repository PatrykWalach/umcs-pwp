# Generated by Django 4.1.4 on 2023-01-25 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0019_alter_post_options_alter_post_order_with_respect_to"),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name="post",
            order_with_respect_to=None,
        ),
    ]