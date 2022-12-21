# Generated by Django 4.0.5 on 2022-12-09 00:29

from django.db import migrations, models
import items.models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_alter_category_description_alter_category_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, unique=True, upload_to=items.models.upload_image),
        ),
    ]