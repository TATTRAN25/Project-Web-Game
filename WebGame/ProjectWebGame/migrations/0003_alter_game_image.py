# Generated by Django 5.1.1 on 2024-10-10 16:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ProjectWebGame", "0002_alter_game_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="image",
            field=models.ImageField(blank=True, upload_to="game_pic/"),
        ),
    ]
