# Generated by Django 5.0.4 on 2024-04-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_bid_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
