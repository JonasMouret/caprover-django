# Generated by Django 3.1.3 on 2020-11-15 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20201115_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagebelier',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
