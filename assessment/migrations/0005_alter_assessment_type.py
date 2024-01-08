# Generated by Django 4.2.6 on 2023-11-08 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0004_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='type',
            field=models.CharField(choices=[('mcq', 'MCQ'), ('short answer', 'Short Answer'), ('essay', 'Essay')], default='mcq', max_length=100),
        ),
    ]
