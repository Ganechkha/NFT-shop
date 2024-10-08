# Generated by Django 5.1.1 on 2024-10-10 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_favorite_nft_remove_favorite_profile'),
        ('favorites', '0001_initial'),
        ('shop', '0004_alter_nftproduct_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(related_name='users_added', through='favorites.Favorite', to='shop.nftproduct'),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
