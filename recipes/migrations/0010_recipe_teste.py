# Generated by Django 4.0.2 on 2022-04-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_remove_recipe_tags_recipe_tags_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='teste',
            field=models.BooleanField(default=False),
        ),
    ]
