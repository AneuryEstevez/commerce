# Generated by Django 4.0.6 on 2022-09-03 19:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_watchlistusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlistUsers',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
