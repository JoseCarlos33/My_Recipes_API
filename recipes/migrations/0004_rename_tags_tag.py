# Generated by Django 4.0.2 on 2022-04-14 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_tags_remove_recipe_tags_recipe_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]
