# Generated by Django 4.2.6 on 2023-11-10 08:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(limit_value=8, message='Password must be atleast 8 characters long.'), django.core.validators.RegexValidator(message='Password must contain one Upper and lower character.', regex='[A-Za-z]'), django.core.validators.RegexValidator(message='Password must contain atleast one digit.', regex='[0-9]'), django.core.validators.RegexValidator(message='Password must contain atleast one special char.', regex='[!@#$%&*]'), django.core.validators.RegexValidator(inverse_match=True, regex='[+-/%]')]),
        ),
    ]
