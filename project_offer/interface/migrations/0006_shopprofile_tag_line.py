# Generated by Django 2.1.5 on 2019-08-18 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0005_auto_20190809_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopprofile',
            name='tag_line',
            field=models.TextField(blank=True, max_length=40),
        ),
    ]