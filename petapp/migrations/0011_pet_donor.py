# Generated by Django 5.0 on 2024-07-03 05:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0010_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='donor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donated_pets', to='petapp.donor'),
        ),
    ]
