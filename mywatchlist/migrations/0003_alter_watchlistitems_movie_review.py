# Generated by Django 4.1 on 2022-09-20 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mywatchlist', '0002_alter_watchlistitems_movie_watched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlistitems',
            name='movie_review',
            field=models.TextField(max_length=600),
        ),
    ]