# Generated by Django 2.1.5 on 2019-06-05 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer_discription',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]