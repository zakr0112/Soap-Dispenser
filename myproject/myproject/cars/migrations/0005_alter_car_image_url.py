# Generated by Django 5.1.4 on 2024-12-31 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_car_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image_url',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
