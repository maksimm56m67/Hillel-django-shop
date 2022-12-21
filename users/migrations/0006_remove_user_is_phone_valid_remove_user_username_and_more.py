# Generated by Django 4.0.5 on 2022-11-09 21:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_phone_valid',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator], verbose_name='email address'),
        ),
    ]