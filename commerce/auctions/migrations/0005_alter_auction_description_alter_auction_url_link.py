# Generated by Django 4.0.4 on 2022-05-02 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auction_url_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='auction',
            name='url_link',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
