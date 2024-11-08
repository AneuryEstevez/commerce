# Generated by Django 4.0.6 on 2022-09-03 00:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_imageurl_alter_listing_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlistUsers',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]