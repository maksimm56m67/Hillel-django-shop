# Generated by Django 4.0.5 on 2022-11-09 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_first_name_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_phone_valid',
            field=models.BooleanField(default=False),
        ),
    ]