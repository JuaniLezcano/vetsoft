# Generated by Django 5.0.4 on 2024-06-05 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_merge_0008_provider_address_0010_alter_pet_breed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.IntegerField(),
        ),
    ]