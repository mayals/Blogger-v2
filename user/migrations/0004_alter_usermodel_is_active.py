# Generated by Django 4.2.9 on 2024-01-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_usermodel_password1_usermodel_password2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]